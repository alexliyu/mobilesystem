"""Admin of lincdm.content"""
from django.contrib import admin
from ..models import Entry
from ..models import Category
from .entry import EntryAdmin
from .category import CategoryAdmin
admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)
