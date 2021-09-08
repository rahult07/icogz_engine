from django.db import models

# Create your models here.

from django.db import models



class app_data(models.Model):
    date = models.TextField(max_length=500)
    country = models.CharField(max_length=500)
    media_source = models.CharField(max_length=200)
    campaign = models.CharField(max_length=200)
    source_name = models.CharField(max_length=200)

    def __str__(self):
        return self.campaign

    class Meta:
        db_table = 'app_data'


class ios_data(models.Model):
    date = models.TextField(max_length=500)
    country = models.CharField(max_length=500)
    media_source = models.CharField(max_length=200)
    campaign = models.CharField(max_length=200)
    source_name = models.CharField(max_length=200)

    def __str__(self):
        return self.campaign

    class Meta:
        db_table = 'ios_data'
