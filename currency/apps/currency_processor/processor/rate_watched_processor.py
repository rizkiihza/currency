from django.apps import apps

from currency.apps.currency_processor.constants import AGGREGATION_PERIOD
from currency.apps.currency_processor.processor.rate_processor import RateProcessor

User = apps.get_model("currency_processor", "User")
RateWatched = apps.get_model("currency_processor", "RateWatched")

class RateWatchedProcessor(object):
    @staticmethod
    def get_all_watched_rate_data_of_user(user, date):
        rate_watched = RateWatched.objects.filter(user=user)

        watchlist_data = {}
        watchlist_data['date'] = date
        watchlist_data['data'] = []

        for rate in rate_watched:
            currency_from = rate.currency_from
            currency_to = rate.currency_to

            rate_data = RateProcessor.get_specific_rate_data(currency_from, currency_to, date)
            watchlist_data['data'].append(rate_data)

        return watchlist_data

    @staticmethod
    def add_rate_to_watched_rate(user_id, currency_from, currency_to):
        user  = User.objects.get(user_id)
        rate_watched, created = RateWatched.get_or_create(user=user, currency_from=currency_from, 
                                                        currency_to=currency_to)
        return created
    
    @staticmethod
    def remove_rate_from_watched_rate(user_id, currency_from, currency_to):
        user, _ = User.get_or_create(user_id)
        rate_watched = RateWatched.objects.get(user=user, currency_from=currency_from, currency_to=currency_to)
        if rate_watched is not None:
            rate_watched.delete()
    