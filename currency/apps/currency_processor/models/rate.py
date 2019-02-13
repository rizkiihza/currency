from django.db import models
from django.utils.timezone import now

# Create your models here.
class Rate(models.Model):
    rate_id = models.IntegerField(primary_key=True,unique=True)

    currency_form = models.CharField(max_length=128)
    currency_to = models.CharField(max_length=128)

    value = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField(auto_now_add=True)



