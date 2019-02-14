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
            Rate.objects.create(currency_from=self.currency_from, currency_to=self.currency_to, value=self.value, 
                                            date=self.today-timedelta(days=day))

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