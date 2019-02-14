from django.apps import apps
from datetime import timedelta
from math import inf

from currency.apps.currency_processor.constants import (
    AGGREGATION_PERIOD
)

Rate = apps.get_model("currency_processor", "Rate")

class RateProcessor(object):
    @staticmethod
    def get_current_rate_data(currency_from, currency_to, date):
        rates = Rate.objects.filter(currency_from=currency_from, currency_to=currency_to, date=date)
        if len(rates) == 0:
            raise Exception("Insufficient data")
        
        return rates[0]

    @staticmethod
    def get_aggregate_period_data(currency_from, currency_to, date):
        start_period = date - timedelta(days=AGGREGATION_PERIOD-1)
        rates = Rate.objects.filter(currency_from=currency_from, currency_to=currency_to, 
                                    date__gte=start_period)

        if len(rates) < AGGREGATION_PERIOD:
            raise Exception("Insufficient data")

        return rates

    @staticmethod
    def calculate_aggregate_period_average(rates):
        if rates is None:
            raise Exception("Insufficient data")
        if len(rates) < AGGREGATION_PERIOD:
            raise Exception("Insufficient data")

        total_sum = 0

        for rate in rates:
            total_sum += rate.value

        return total_sum / AGGREGATION_PERIOD

    @staticmethod
    def calculate_aggregate_period_variance(rates):
        if rates is None:
            raise Exception("Insufficient data")
        if len(rates) < AGGREGATION_PERIOD:
            raise Exception("Insufficient data")

        rate_max = -1*inf
        rate_min = inf

        for rate in rates:
            rate_max = max(rate.value, rate_max)
            rate_min = min(rate.value, rate_min)

        return rate_max - rate_min
        
    @staticmethod
    def get_specific_rate_data(currency_form, currency_to, date):
        rate_data = {}
        rate_data['from'] = currency_form
        rate_data['to'] = currency_to

        average_tag = "%d-day avg" % (AGGREGATION_PERIOD)
        variance_tag = "%d-day avg" % (AGGREGATION_PERIOD)
        try:
            rate_data['rate'] = RateProcessor.get_current_rate_data(currency_form, currency_to, date)

            rates = RateProcessor.get_aggregate_period_data(currency_form, currency_to, date)
            
            rate_data[average_tag] = RateProcessor.calculate_aggregate_period_average(rates)
            rate_data[variance_tag] = RateProcessor.calculate_aggregate_period_variance(rates)

        except:
            rate_data['rate'] = 'Insufficient data'
            rate_data[average_tag] = 'Insufficient data'
            rate_data[variance_tag] = 'Insufficient data'

        finally:
            return rate_data