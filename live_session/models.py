from django.db import models
from django.db.models import JSONField

class Session(models.Model):
    session_id = models.BigIntegerField(primary_key=True, unique=True) 

    def __str__(self):
        return str(self.session_id)

class Position(models.Model):
    session = models.OneToOneField(Session, related_name='positions', on_delete=models.CASCADE)
    data = JSONField()  

class Account(models.Model):
    session = models.OneToOneField(Session, related_name='account', on_delete=models.CASCADE)
    data = JSONField()  

class Order(models.Model):
    session = models.OneToOneField(Session, related_name='orders', on_delete=models.CASCADE)
    data = JSONField()  

class Risk(models.Model):
    session = models.OneToOneField(Session, related_name='risk', on_delete=models.CASCADE)
    data = JSONField()  

class MarketData(models.Model):
    session = models.OneToOneField(Session, related_name='market_data', on_delete=models.CASCADE)
    data = JSONField()  

