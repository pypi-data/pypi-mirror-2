# -*- coding: utf-8 -*-
"""Placeholder so that tests are loaded."""

from django.contrib.sites.models import Site
from django.db import models
from skins.skin import get_skin_choices

SKINS = get_skin_choices()

class Skin(models.Model):
    name = models.CharField(max_length=20, choices=SKINS)
    site = models.ForeignKey(Site, related_name='skin')

    def __unicode__(self):
        return u"%s" % self.name
