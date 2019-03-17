from django.forms import forms
from django import forms
class ImageSearch(forms.Form):
    search=forms.CharField(max_length=1000)
    center=forms.CharField(max_length=1000, required=False)
    keywords=forms.CharField(max_length=500, required=False)
    location=forms.CharField(max_length=500, required=False)
    nasa_id=forms.CharField(max_length=300, required=False)
    photographer=forms.CharField(max_length=300, required=False)
    title=forms.CharField(max_length=500, required=False)
    year_start=forms.IntegerField(required=False)
    year_end=forms.IntegerField(required=False)

   