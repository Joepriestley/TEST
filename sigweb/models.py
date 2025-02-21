from django.db import models  # type: ignore
from django.contrib.gis.gdal import DataSource  # type: ignore
from django.contrib.gis.geos import GEOSGeometry  # type: ignore
from django.contrib.gis.db import models as gis_models  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
import geopandas as gpd
import os
import glob
import zipfile
from sqlalchemy import *
from sqlalchemy.sql import text 
import pandas as pd
"""
class Province(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Provinces'

class Cercle(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cercles")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Cercles'

class Commune(models.Model):
    name = models.CharField(max_length=50)
    cercle = models.ForeignKey(Cercle, on_delete=models.CASCADE, related_name="communes")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Communes'



class Douar(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name="communes")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Douars'

"""

class Parcelle(models.Model):
    num_dossie = models.CharField(max_length=255, blank=True)
    num_parcel = models.CharField(max_length=255, blank=True)
    province= models.CharField(max_length=255, blank=True)
    commune= models.CharField(max_length=255, blank=True)
    douar= models.CharField(max_length=255, blank=True)
    cercle= models.CharField(max_length=255, blank=True)
    consistanc = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    nb_de_faca = models.IntegerField()
    fchier_dwg = models.FileField(upload_to='dwg/', blank=True, null=True)
    fchier_pdf = models.FileField(upload_to='pdf/', blank=True, null=True)
    geometry = gis_models.PolygonField(srid=4326)  # Géométrie exploitée par PostGIS


    def __str__(self):
        return f"Parcelle {self.num_dossie}"

    class Meta:
        db_table = 'Parcelles'


class Proprietaire(models.Model):
    parcelle =models.ForeignKey(Parcelle, on_delete=models.CASCADE, related_name='proprietaires')
    nom=models.CharField(max_length=255, blank=True)
    prenom = models.CharField(max_length=255, blank=True)
    CIN = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=255, blank=True)
    document=models.FileField(upload_to='proprietaire/', blank=True, null=True)
    
    def __str__(self):
        return self.nom



""" ******************************************************* Uploader des données*********************************************************"""

conn_str = "postgresql://postgres:123456789@localhost:5432/globetude"
    

class Shp(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    file = models.FileField(upload_to='%Y/%m/%d')
    date = models.DateField(default=datetime.date.today, blank=True)
    
    def __str__(self):
        return f"{self.name}"

@receiver(post_save, sender=Shp)
def publish_data(sender, instance, created, **kwargs):
    file = instance.file.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    name = instance.name

    # extract zipfile
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(file_path)

    os.remove(file)  # remove zip file

    shp = glob.glob(r'{}/**/*.shp'.format(file_path),
                    recursive=True)  # to get shp
    try:
        req_shp = shp[0]
        gdf = gpd.read_file(req_shp)  # make geodataframe
        # Vérification et définition du CRS
        if gdf.crs is None:
            gdf.set_crs("EPSG:4326", inplace=True)
        else:
            gdf = gdf.to_crs("EPSG:4326")
            
        engine = create_engine(conn_str)
        """
        with engine.connect() as conn:
            # Récupérez les ID valides de la table de référence
            valid_douars = pd.read_sql('SELECT id FROM "public"."Douars"', conn)['id'].tolist()

        # Filtrer les données pour correspondre aux clés étrangères valides
        gdf = gdf[gdf['douar_id'].isin(valid_douars)]
        """

        gdf.to_postgis(
            con=engine,
            schema='public',
            name=name,
            if_exists="append")

        for s in shp:
            os.remove(s)

    except Exception as e:
        for s in shp:
            os.remove(s)

        instance.delete()
        print("There is problem during shp upload: ", e)




""" ********************************************************************************************************************************************************"""