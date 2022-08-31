from django.db import models

# Create your models here.

class Stock(models.Model):
    name=models.CharField(max_length=200)
    symbol=models.CharField(max_length=200)
    opened=models.CharField(max_length=200)
    high=models.CharField(max_length=200)
    low=models.CharField(max_length=200)
    price=models.CharField(max_length=200)
    volume=models.CharField(max_length=200)
    lastTradingDay=models.CharField(max_length=200)
    previousClose=models.CharField(max_length=200)
    change=models.CharField(max_length=200)
    changePercent=models.CharField(max_length=200)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name