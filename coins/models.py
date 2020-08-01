from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.
class Coin(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=64)
    price = models.FloatField(default=0)
    price_change = models.FloatField(blank=True, default=0, null=True)
    price_btc = models.FloatField(default=0)
    price_btc_change = models.FloatField(default=0)
    social_score = models.FloatField(default=0)
    social_score_change = models.FloatField(blank=True, default=0, null=True)
    market_cap = models.FloatField(default=0)
    market_cap_change = models.FloatField(blank=True, default=0, null=True)
    total_volume = models.FloatField(blank=True, default=0, null=True)
    total_volume_change = models.FloatField(blank=True, default=0, null=True)
    history = HistoricalRecords()
    def __str__(self):
        return f"{self.name} ({self.symbol})"
