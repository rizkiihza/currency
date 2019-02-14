from currency.apps.currency_processor.utils.date_converter import DateConverter
from currency.apps.currency_processor.processor.rate_processor import RateProcessor
from currency.apps.currency_processor.processor.rate_watched_processor import RateWatchedProcessor


class DictionaryConverter(object):
    # convert date in watchlist_data to string
    def convert_watchlist_data_date_to_string(watchlist_data):
        watchlist_data['date'] = DateConverter.convert_to_string_from_datetime(watchlist_data['date'])
        return watchlist_data

    # convert all date in historical data in rate data to string
    def convert_historical_data_date_to_string(rate_data):
        if 'historical_data' in rate_data:
            for i in range(len(rate_data['historical_data'])):
                date = rate_data['historical_data'][i]['date']
                rate_data['historical_data'][i]['date'] = DateConverter.convert_to_string_from_datetime(date)
        return rate_data
