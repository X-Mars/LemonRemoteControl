from django.db import models

# Create your models here.

class Zabbix(models.Model):
    home_url = models.CharField(max_length=1000, null=True)
    username = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)