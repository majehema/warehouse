from django.contrib import admin
from .models import Article, Shelf, Warehouse

# Register your models here.
admin.site.register(Article)
admin.site.register(Shelf)
admin.site.register(Warehouse)