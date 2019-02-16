from django.apps import apps
from datetime import timedelta
from math import inf

from currency.apps.currency_processor.utils.date_converter import DateConverter
from currency.apps.currency_processor.constants import (
    AGGREGATION_PERIOD,
    MESSAGE_INSUFFICIENT_DATA
)

Rate = apps.get_model("currency_processor", "Rate")

class RateProcessor(object):
    @staticmethod
    def insert_rate_data(currency_from, currency_to, value, date):
        # check wether data already exist
        rates = Rate.objects.filter(currency_from=currency_from, currency_to=currency_to, date=date)

        # if data exist, then override that data
        if len(rates) > 0:
            rates[0].value = value
            rates[0].save()
            return rates[0]
        
        rate, _ = Rate.objects.get_or_create(currency_from=currency_from, currency_to=currency_to, value=value, date=date)
        return rate

    @staticmethod
    def get_current_rate_data(currency_from, currency_to, date):
        rates = Rate.objects.filter(currency_from=currency_from, currency_to=currency_to, date=date)
        if len(rates) == 0:
            raise Exception(MESSAGE_INSUFFICIENT_DATA)
        
        return rates[0]

    # return data from AGGREGATION_PERIOD range
    @staticmethod
    def get_aggregate_period_data(currency_from, currency_to, date):
        start_period = date - timedelta(days=AGGREGATION_PERIOD-1)
        end_period = date
        rates = Rate.objects.filter(currency_from=currency_from, currency_to=currency_to, 
                                    date__gte=start_period, date__lte=end_period)

        if len(rates) < AGGREGATION_PERIOD:
            raise Exception(MESSAGE_INSUFFICIENT_DATA)

        return rates

    @staticmethod
    def calculate_aggregate_period_average(rates):
        if rates is None:
            raise Exception(MESSAGE_INSUFFICIENT_DATA)
        if len(rates) < AGGREGATION_PERIOD:
            raise Exception(MESSAGE_INSUFFICIENT_DATA)

        total_sum = 0

        for rate in rates:
            total_sum += float(rate.value)

        return total_sum / AGGREGATION_PERIOD

    @staticmethod
    def calculate_aggregate_period_variance(rates):
        if rates is None:
            raise Exception(MESSAGE_INSUFFICIENT_DATA)
        if len(rates) < AGGREGATION_PERIOD:
            raise Exception(MESSAGE_INSUFFICIENT_DATA)

        rate_max = -1*inf
        rate_min = inf

        for rate in rates:
            rate_max = max(float(rate.value), rate_max)
            rate_min = min(float(rate.value), rate_min)

        return rate_max - rate_min
    
    # get historical data over AGGREGATION_PERIOD range
    @staticmethod
    def get_historical_data(currency_from, currency_to, date):
        historical_data_dict = {}

        list_of_dates = [DateConverter.convert_to_string_from_datetime((date - timedelta(days=day))) 
                                for day in range(AGGREGATION_PERIOD)]

        rates = Rate.objects.filter(currency_from=currency_from, currency_to=currency_to, 
                                        date__gte=date-timedelta(days=AGGREGATION_PERIOD-1))
        for rate in rates:
            date_string = DateConverter.convert_to_string_from_datetime(rate.date)
            if date_string in list_of_dates:
                historical_data_dict[rate.date] = float(rate.value)

        
        historical_data_list = [{'date': date, 'rate': historical_data_dict[date]} for date in historical_data_dict]

        return sorted(historical_data_list, key= lambda element: element['date'])


    # creating dictionary data for a specific rate
    # can also include historical data using with_historical_data parameter
    @staticmethod
    def get_specific_rate_data(currency_from, currency_to, date, with_historical_data=False):
        rate_data = {}
        rate_data['from'] = currency_from
        rate_data['to'] = currency_to

        average_tag = "%d-day avg" % (AGGREGATION_PERIOD)
        variance_tag = "%d-day variance" % (AGGREGATION_PERIOD)

        try:
            current_rate = RateProcessor.get_current_rate_data(currency_from, currency_to, date)
            rate_data['rate'] = float(current_rate.value)
            rates = RateProcessor.get_aggregate_period_data(currency_from, currency_to, date)
            
            rate_data[average_tag] = RateProcessor.calculate_aggregate_period_average(rates)
            rate_data[variance_tag] = RateProcessor.calculate_aggregate_period_variance(rates)

        except:
            rate_data['rate'] = float(current_rate.value) if current_rate is not None else MESSAGE_INSUFFICIENT_DATA
            rate_data[average_tag] = MESSAGE_INSUFFICIENT_DATA
            rate_data[variance_tag] = MESSAGE_INSUFFICIENT_DATA

        finally:
            if with_historical_data:
                rate_data['historical_data'] = RateProcessor.get_historical_data(currency_from, currency_to, date)
            return rate_data