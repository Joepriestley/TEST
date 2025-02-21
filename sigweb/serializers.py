from rest_framework import serializers
from django.db import models
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from sigweb.models import  Parcelle
"""
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'

class CercleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cercle
        fields = '__all__'


class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = '__all__'


class DouarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Douar
        fields = '__all__'

        """

class ParcelleSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Parcelle
        geo_field='geometry'
        fields = '__all__'
