# -*- mode: python; coding: utf-8; -*-

from models import FlashCard
from django.contrib import admin

class FlashCardAdmin(admin.ModelAdmin):
    fields = ['front', 'back', 'user']
    list_display = ('front', 'back', 'user', 'next_practice', 'times_practiced',
                   'easy_factor')

admin.site.register(FlashCard, FlashCardAdmin)
