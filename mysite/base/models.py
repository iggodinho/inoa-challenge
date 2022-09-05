from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class Stock(models.Model):
    name=models.CharField(max_length=200)
    symbol=models.CharField(max_length=200,db_index=True,default='any_name')
    opened=models.CharField(max_length=200)
    high=models.CharField(max_length=200)
    low=models.CharField(max_length=200)
    close=models.CharField(max_length=200)
    interval=models.CharField(max_length=200)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symbol