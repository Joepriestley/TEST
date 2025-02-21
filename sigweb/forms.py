from django import forms
from .models import Proprietaire, Parcelle 

class ProprietaireForm(forms.ModelForm):
    class Meta:
        model = Proprietaire
        fields = ['nom', 'prenom', 'CIN', 'telephone', 'document']  # Ajoute les champs nécessaires

class ParcelleForm(forms.ModelForm):
    class Meta:
        model = Parcelle
        fields = ['fchier_dwg', 'fchier_pdf']  # Ajoute les champs nécessaires