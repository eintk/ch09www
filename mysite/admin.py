# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mysite import models
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('nickname','message','enabled','pub_time')
    ordering = ('-pub_time',)


admin.site.register(models.Mood)
admin.site.register(models.Post,PostAdmin)
admin.site.register(models.Profile)
