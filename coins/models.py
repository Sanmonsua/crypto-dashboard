from django.db import models

# Create your models here.
class Coin(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=64)
    price = models.FloatField(default=0)
    social_score = models.FloatField(default=0)
    market_cap = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} ({self.symbol})"
