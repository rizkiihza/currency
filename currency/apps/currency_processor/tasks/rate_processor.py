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
        last_week_day = date - timedelta(day=AGGREGATION_PERIOD)
        rates = Rate.objects.filter(currency_from=currency_from, currency_to=currency_to, 
                                    date__gte=last_week_day)

        return rates

    @staticmethod
    def calculate_aggregate_period_average(rates):
        if len(rates) < AGGREGATION_PERIOD:
            raise Exception("Insufficient data")

        total_sum = 0

        for rate in rates:
            total_sum += rate.value

        return total_sum / AGGREGATION_PERIOD

    @staticmethod
    def calculate_aggregate_period_variance(rates):
        if len(rates) < AGGREGATION_PERIOD:
            raise Exception("Insufficient data")

        rate_max = -1*inf
        rate_min = inf

        for rate in rates:
            rate_max = max(rate.value, rate_max)
            rate_min = min(rate.value, rate_min)

        return rate_max - rate_min
        