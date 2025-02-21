from django.urls import path 
from . import views


app_name="sigweb"
urlpatterns=[
     path('',views.Acueil,name="acueil"),
     path('Parcelle/',views.ParcelleList.as_view(),name="parcelle"),
     path('index/',views.index,name="carte"),
     path('liste_parcelle/',views.liste_parcelle,name="liste_parcelle"),
     
     path("LISTE/", views.liste_parcelles, name="liste_parcelles"),

     #pour avoir les informations de la parcelle en detail
    path("parcelle/<int:parcelle_id>/", views.details_parcelle, name="details_parcelle"),
     #pour avoir la geometry sur leaflet
    path('parcelles/<int:pk>/', views.ParcelleDetailView.as_view(), name="parcelle-Details"),
    #url des pour le telechargement
    path('LISTE/dwg/<str:filename>/', views.download_dwg1, name='download_dwg'),
    path('LISTE/pdf/<str:filename>/', views.download_pdf1, name='download_dwg'),
    path('parcelle/<int:parcelle_id>/proprietaire/<str:filename>/', views.download_proprietaire, name='download_proprietaire'),
    path('parcelle/<int:parcelle_id>/dwg/<str:filename>/', views.download_dwg, name='download_dwg'),
    path('parcelle/<int:parcelle_id>/pdf/<str:filename>/', views.download_pdf, name='download_pdf'),


    #formulaire de modification
    #path('parcelle/<int:parcelle_id>/modifier_proprietaire/', views.modifier_proprietaire, name='modifier_proprietaire'),
    path('parcelle/<int:parcelle_id>/modifier_fichier_dwg/', views.modifier_des_fichier_DWG, name='modifier_fichier'),
    path('modifier-proprietaire/<int:parcelle_id>/', views.modifier_proprietaire, name="modifier_proprietaire"),

     ]

