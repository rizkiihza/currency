from django.apps import apps

from currency.apps.currency_processor.constants import AGGREGATION_PERIOD
from currency.apps.currency_processor.tasks.rate_processor import RateProcessor

User = apps.get_model("currency_processor", "User")
RateWatched = apps.get_model("currency_processor", "RateWatched")

class RateWatchedProcessor(object):
    @staticmethod
    def get_specific_rate_data(currency_form, currency_to, date):
        rate_data = {}
        rate_data['from'] = currency_form
        rate_data['to'] = currency_to

        average_tag = "%d-day avg" % (AGGREGATION_PERIOD)
        variance_tag = "%d-day avg" % (AGGREGATION_PERIOD)
        try:
            rate_data['rate'] = RateProcessor.get_current_rate_data(currency_form, currency_to, date)

            rates = RateProcessor().get_aggregate_period_data(currency_form, currency_to, date)
            
            rate_data[average_tag] = RateProcessor.calculate_aggregate_period_average(rates)
            rate_data[variance_tag] = RateProcessor.calculate_aggregate_period_variance(rates)

        except:
            rate_data['rate'] = 'Insufficient data'
            rate_data[average_tag] = 'Insufficient data'
            rate_data[variance_tag] = 'Insufficient data'

        finally:
            return rate_data

    @staticmethod
    def get_all_watched_rate_data_of_user(user, date):
        rate_watched = RateWatched(user=user)

        watchlist_data = {}
        watchlist_data['date'] = date
        watchlist_data['data'] = []

        for rate in rate_watched:
            currency_from = rate.currency_from
            currency_to = rate.currency_to

            rate_data = RateWatchedProcessor.get_specific_rate_data(currency_from, currency_to, date)
            watchlist_data['data'].append(rate_data)

    