# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from google.appengine.ext import db


class DbTemplate(db.Model):
    name    = db.StringProperty()
    title   = db.StringProperty()
    content = db.TextProperty()

    def __repr__(self):
        return "<DbTemplate: %s>" % self.name
