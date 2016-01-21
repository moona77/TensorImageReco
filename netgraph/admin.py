#-*- coding: utf-8 -*-
from django.contrib import admin
from .models import Nodeset, Network,NewsData, Links

# Register your models here.

admin.site.register(Nodeset)
admin.site.register(Network)
admin.site.register(NewsData)
admin.site.register(Links)