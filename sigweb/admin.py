from django.contrib import admin

from .models import  Parcelle, Shp, Proprietaire
admin.site.register(Parcelle)
admin.site.register(Proprietaire)

admin.site.register(Shp)

