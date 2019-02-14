from django.db import models
from django.apps import apps

class User(models.Model):
    user_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return "%d - %s" % (self.user_id, self.name)

class RateWatched(models.Model):
    rate_watched_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    currency_from = models.CharField(max_length=128)
    currency_to = models.CharField(max_length=128)

    def __str__(self):
        return "user_id: %d - from %s to %s" % (self.user.user_id, self.currency_from, self.currency_to)