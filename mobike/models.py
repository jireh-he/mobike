# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Mobikedata(models.Model):
    mbkid = models.CharField(db_column='MBKID', primary_key=True, max_length=255)  # Field name made lowercase.
    mbkno = models.CharField(db_column='MBKNO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    flag = models.CharField(db_column='FLAG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    starttime = models.CharField(max_length=255, blank=True, null=True)
    startlng = models.FloatField(blank=True, null=True)
    startlat = models.FloatField(blank=True, null=True)
    endtime = models.CharField(max_length=255, blank=True, null=True)
    endlng = models.FloatField(blank=True, null=True)
    endlat = models.FloatField(blank=True, null=True)
    pathstr = models.TextField(blank=True, null=True)
    costtime = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mobikedata'