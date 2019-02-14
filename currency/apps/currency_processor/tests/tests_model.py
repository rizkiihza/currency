from django.test import TestCase
from django.apps import apps
from django.utils import timezone

User = apps.get_model("currency_processor", "User")
RateWatched = apps.get_model("currency_processor", "RateWatched")
Rate = apps.get_model("currency_processor", "Rate")

# Create your tests here.
class TestUserModel(TestCase):

    def test_user_added_by_one(self):
        initital_user_count = len(User.objects.all())
        User.objects.create(user_id=1, name="Rizki Ihza")
        final_user_count = len(User.objects.all())

        self.assertEqual(final_user_count, initital_user_count+1)

    def test_user_attribute(self):
        user_id = 2
        name = "Fathurrahman"
        user = User.objects.create(user_id=user_id, name=name)

        self.assertEqual(user.user_id, user_id)
        self.assertEqual(user.name, name)

class TestRateWatchedModel(TestCase):
    def setUp(self):
        self.user, _ = User.objects.get_or_create(user_id=1, name="Rizki Ihza")

    def test_rate_watched_added_by_one(self):
        initial_rate_watched_count = len(RateWatched.objects.all())

        currency_from = "USD"
        currency_to = "IDR"

        rate_watched = RateWatched.objects.create(user=self.user, currency_from=currency_from,
                                                    currency_to=currency_to)
        final_rate_watched_count = len(RateWatched.objects.all())

        self.assertEqual(final_rate_watched_count, initial_rate_watched_count+1)

    def test_rate_watched_attribute(self):
        currency_from = "USD"
        currency_to = "IDR"
        rate_watched = RateWatched.objects.create(user=self.user, currency_from=currency_from,
                                                    currency_to=currency_to)

        self.assertEqual(rate_watched.user, self.user)
        self.assertEqual(rate_watched.currency_from, currency_from)
        self.assertEqual(rate_watched.currency_to, currency_to)

class TestRateModel(TestCase):
    def test_rate_added_by_one(self):
        initial_rate_count = len(Rate.objects.all())

        currency_from = "USD"
        currency_to = "IDR"
        value = 15000

        rate = Rate.objects.create(currency_from=currency_from, currency_to=currency_to,
                                    value=value)

        final_rate_count = len(Rate.objects.all())

        self.assertEqual(final_rate_count, initial_rate_count+1)

    def test_rate_attribute(self):
        currency_from = "USD"
        currency_to = "IDR"
        value = 15000

        rate, _ = Rate.objects.get_or_create(currency_from=currency_from, currency_to=currency_to,
                                                value=value)

        self.assertEqual(rate.currency_from, currency_from)
        self.assertEqual(rate.currency_to, currency_to)
        self.assertEqual(rate.value, value)

    def test_rate_date(self):
        currency_from = "USD"
        currency_to = "IDR"
        value = 15000

        rate, _ = Rate.objects.get_or_create(currency_from=currency_from, currency_to=currency_to,
                                                value=value)

        today = timezone.now().date()        
        self.assertEqual(rate.date, today)