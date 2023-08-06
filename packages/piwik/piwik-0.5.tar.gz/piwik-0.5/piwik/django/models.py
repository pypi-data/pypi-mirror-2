# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.sites.models import Site

class PiwikSite(models.Model):
    id_site = models.IntegerField()
    site = models.ForeignKey(Site, unique=True)

    def __unicode__(self):
        return 'Site %s' % self.id_site
