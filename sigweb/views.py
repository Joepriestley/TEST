from django.shortcuts import render, get_object_or_404, redirect
from sigweb.models import Parcelle, Proprietaire
from sigweb.serializers import ParcelleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status 
from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.
from django.http import FileResponse, JsonResponse, Http404

from django.conf import settings
import os
from .forms import ProprietaireForm, ParcelleForm
from django.template.loader import render_to_string



class ParcelleList(generics.ListCreateAPIView):
    queryset= Parcelle.objects.all()
    serializer_class =ParcelleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['num_dossie', 'num_parcel', 'consistanc']
    search_fields = ['num_parcel', 'num_dossie']
    ordering_fields = ['num_parcel']
    ordering = ['num_parcel']

def Acueil(request):
    return render(request, 'sigweb/Acueil.html')

def index(request):
    return render(request, 'sigweb/index.html')

def liste_parcelle(request):
    return render(request, 'sigweb/liste_parcelle.html')



def liste_parcelles(request):
    parcelles = Parcelle.objects.all()
    return render(request, "sigweb/liste_parcelles.html", {"parcelles": parcelles})

def details_parcelle(request, parcelle_id):
    parcelle = get_object_or_404(Parcelle, id=parcelle_id)
    proprietaire = Proprietaire.objects.filter(parcelle=parcelle).first()
    return render(request, "sigweb/details_parcelle.html", {"parcelle": parcelle, "proprietaire": proprietaire})


class ParcelleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset= Parcelle.objects.all()
    serializer_class = ParcelleSerializer


def download_dwg1(request,  filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'dwg', filename)  # adapte le chemin selon ton organisation
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    else:
        raise Http404("Fichier non trouvé")
def download_pdf1(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'pdf', filename)  # adapte le chemin selon ton organisation
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    else:
        raise Http404("Fichier non trouvé")

def download_dwg(request,  parcelle_id, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'dwg', filename)  # adapte le chemin selon ton organisation
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    else:
        raise Http404("Fichier non trouvé")
    

def download_pdf(request,  parcelle_id, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'pdf', filename)  # adapte le chemin selon ton organisation
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    else:
        raise Http404("Fichier non trouvé")
    
def download_proprietaire(request, parcelle_id, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'proprietaire', filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    else:
        raise Http404("Fichier non trouvé")



def modifier_proprietaire(request, parcelle_id):
    parcelle = get_object_or_404(Parcelle, id=parcelle_id)
    
    proprietaire = parcelle.proprietaires.first() if hasattr(parcelle, 'proprietaires') else None

    if request.method == "POST":
        form = ProprietaireForm(request.POST, request.FILES, instance=proprietaire)  # ✅ Ajout de request.FILES
        if form.is_valid():
            proprietaire = form.save(commit=False)
            proprietaire.parcelle = parcelle  # Associer à la parcelle
            proprietaire.save()
            return redirect('sigweb:details_parcelle', parcelle_id=parcelle.id)
    else:
        form = ProprietaireForm(instance=proprietaire)

    return render(request, 'sigweb/modifier_proprietaire.html', {'form': form, 'parcelle': parcelle})
    


def modifier_des_fichier_DWG(request, parcelle_id):
    parcelle = get_object_or_404(Parcelle, id=parcelle_id)

    if request.method == "POST":
        form = ParcelleForm(request.POST, request.FILES, instance=parcelle)  # ✅ Ajout de request.FILES
        if form.is_valid():
            parcelle= form.save(commit=False)
            parcelle.save()
            return redirect('sigweb:details_parcelle', parcelle_id=parcelle.id)
    else:
        form = ParcelleForm(instance=parcelle)

    return render(request, 'sigweb/modifier_fichier_dwg.html', {'form': form, 'parcelle': parcelle})



# def modifier_proprietaire(request, parcelle_id):
#     parcelle = get_object_or_404(Parcelle, id=parcelle_id)
#     proprietaire = parcelle.proprietaires.first() if hasattr(parcelle, 'proprietaires') else None

#     if request.method == "POST":
#         form = ProprietaireForm(request.POST, request.FILES, instance=proprietaire)
#         if form.is_valid():
#             proprietaire = form.save(commit=False)
#             proprietaire.parcelle = parcelle  # Associer le propriétaire à la parcelle
#             proprietaire.save()
#             print("✅ Propriétaire enregistré avec succès !")  # Message de débogage
#             return JsonResponse({"success": True})
#         else:
#             print("❌ Erreur de validation :", form.errors)  # Afficher les erreurs de validation
    
#     else:
#         form = ProprietaireForm(instance=proprietaire)

#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         html = render_to_string('sigweb/modifier_proprietaire.html', {'form': form, 'parcelle': parcelle}, request)
#         return JsonResponse({"html": html})

#     return render(request, 'sigweb/modifier_proprietaire.html', {'form': form, 'parcelle': parcelle})





# def modifier_proprietaire(request, parcelle_id):
#     parcelle = get_object_or_404(Parcelle, id=parcelle_id)
#     proprietaire = parcelle.proprietaires.first() if hasattr(parcelle, 'proprietaires') else None

#     if request.method == "POST":
#         form = ProprietaireForm(request.POST, request.FILES, instance=proprietaire)
#         if form.is_valid():
#             proprietaire = form.save(commit=False)
#             proprietaire.parcelle = parcelle  # Associer à la parcelle
#             proprietaire.save()
#             return JsonResponse({"success": True})  # Return success for AJAX
#         else:
#             return JsonResponse({"success": False, "errors": form.errors})

#     else:
#         form = ProprietaireForm(instance=proprietaire)
#         return render(request, "sigweb/modifier_proprietaire_form.html", {"form": form, "parcelle": parcelle})
