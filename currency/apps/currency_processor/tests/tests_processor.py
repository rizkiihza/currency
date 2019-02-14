from django.apps import apps
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from currency.apps.currency_processor.processor.rate_processor import RateProcessor
from currency.apps.currency_processor.processor.rate_watched_processor import RateWatchedProcessor
from currency.apps.currency_processor.constants import AGGREGATION_PERIOD

User = apps.get_model("currency_processor", "User")
RateWatched = apps.get_model("currency_processor", "RateWatched")
Rate = apps.get_model("currency_processor", "Rate")

class RateProcessorTestFullData(TestCase):
    def setUp(self):
        self.currency_from = "USD"
        self.currency_to = "IDR"
        self.value = 15000
        self.today = timezone.now().date()
        for day in range(AGGREGATION_PERIOD):
            date = self.today - timedelta(days=day)
            Rate.objects.create(currency_from=self.currency_from, currency_to=self.currency_to, value=self.value, 
                                            date=date)

        self.rates = Rate.objects.all()
            
    def test_number_of_rate(self):
        self.assertEqual(len(self.rates), AGGREGATION_PERIOD)

    def test_get_current_rate_data(self):
        rate = RateProcessor.get_current_rate_data(self.currency_from, self.currency_to, self.today)
        self.assertTrue(rate is not None)
        self.assertEqual(rate.currency_from, self.currency_from)
        self.assertEqual(rate.currency_to, self.currency_to)
        self.assertEqual(rate.value, self.value)
        self.assertEqual(rate.date, self.today)


    def test_get_aggregate_period_data(self):
        rates = RateProcessor.get_aggregate_period_data(self.currency_from, self.currency_to, self.today)
        self.assertEqual(len(rates), AGGREGATION_PERIOD)

    def test_average_data(self):
        rates = RateProcessor.get_aggregate_period_data(self.currency_from, self.currency_to, self.today)
        average = RateProcessor.calculate_aggregate_period_average(rates)
        self.assertEqual(average, self.value)

    def test_variance_data(self):
        rates = RateProcessor.get_aggregate_period_data(self.currency_from, self.currency_to, self.today)
        variance = RateProcessor.calculate_aggregate_period_variance(rates)
        self.assertEqual(variance, 0)
    
    def test_get_historical_data(self):
        historical_data = RateProcessor.get_historical_data(self.currency_from, self.currency_to, self.today)
        for data in historical_data:
            print(data)
        self.assertEqual(len(historical_data), AGGREGATION_PERIOD)

class RateProcessorTestEmptyData(TestCase):
    def setUp(self):
        self.currency_from = "USD"
        self.currency_to = "IDR"
        self.today = timezone.now().date()
    
    def test_number_of_rate(self):
        rates = Rate.objects.all()
        self.assertEqual(len(rates), 0)

    def test_current_rate_data(self):
        with self.assertRaises(Exception):
            RateProcessor.get_current_rate_data(self.currency_from, self.currency_to, self.today)

    def test_get_aggregate_period_data(self):
        with self.assertRaises(Exception):
            RateProcessor.get_aggregate_period_data(self.currency_from, self.currency_to, self.today)

    def test_calculate_average_data(self):
        rates = None
        with self.assertRaises(Exception):
            rates = RateProcessor.get_aggregate_period_data(self.currency_from, self.currency_to, self.today)

        with self.assertRaises(Exception):
            average = RateProcessor.calculate_aggregate_period_average(rates)

    def test_calculate_variance_data(self):
        rates = None
        with self.assertRaises(Exception):
            rates = RateProcessor.get_aggregate_period_data(self.currency_from, self.currency_to, self.today)

        with self.assertRaises(Exception):
            rates = RateProcessor.calculate_aggregate_period_average(rates)

    def test_get_historical_data(self):
        historical_data = RateProcessor.get_historical_data(self.currency_from, self.currency_to, self.today)
        self.assertEqual(len(historical_data), 0)

class RateWatchedProcessorTestEmptyData(TestCase):
    def setUp(self):
        self.user = User.objects.create(user_id=1, name="Rizki Ihza")

    def test_rate_watched_count(self):
        rates_watched = RateWatched.objects.filter(user=self.user)
        self.assertEqual(len(rates_watched), 0)

    def test_get_all_watched_rate_data_of_user(self):
        today = timezone.now().today()

        watchlist_data = RateWatchedProcessor.get_all_watched_rate_data_of_user(self.user, today)

        self.assertTrue('date' in watchlist_data)
        self.assertEqual(watchlist_data['date'], today)
        self.assertEqual(len(watchlist_data['data']), 0)

class RateWatchedProcessorTestFullData(TestCase):
    def setUp(self):
        self.user = User.objects.create(user_id=1, name="Rizki Ihza")

        self.currency_from = "USD"
        self.currency_to = "IDR"
        self.value = 15000
        self.today = timezone.now().date()

        self.rate_watched = RateWatched.objects.create(user=self.user, currency_from=self.currency_from,
                                                        currency_to=self.currency_to)

        for day in range(AGGREGATION_PERIOD):
            Rate.objects.create(currency_from=self.currency_from, currency_to=self.currency_to,
                                    value=self.value, date=self.today - timedelta(days=day))

    def test_rate_watched_amount(self):
        rates_watched = RateWatched.objects.filter(user=self.user)
        self.assertEqual(len(rates_watched), 1)

    def test_get_all_watched_rate_data_of_user(self):
        watchlist_data = RateWatchedProcessor.get_all_watched_rate_data_of_user(self.user, self.today)

        self.assertTrue('date' in watchlist_data)
        self.assertEqual(watchlist_data['date'], self.today)
        self.assertEqual(len(watchlist_data['data']), 1)

        rate_data = watchlist_data['data'][0]
        average_tag = "%d-day avg" % (AGGREGATION_PERIOD)
        variance_tag = "%d-day variance" % (AGGREGATION_PERIOD)

        self.assertEqual(rate_data['rate'], self.value)
        self.assertEqual(rate_data[average_tag], self.value)
        self.assertEqual(rate_data[variance_tag], 0)