from django.db import models
from django.forms import forms
from django import forms
# Create your models here.

class Search(models.Model):
    search=models.CharField(max_length=1000)
    center=models.CharField(max_length=1000, blank=True, null=True)
    keywords=models.CharField(max_length=500, blank=True, null=True)
    location=models.CharField(max_length=500, blank=True, null=True)
    nasa_id=models.CharField(max_length=300, blank=True, null=True)
    photographer=models.CharField(max_length=300, blank=True, null=True)
    title=models.CharField(max_length=500, blank=True, null=True)
    year_start=models.IntegerField(blank=True, null=True)
    year_end=models.IntegerField(blank=True, null=True)

class ImageResult(models.Model):
    description=models.TextField()
    date_created=models.DateTimeField()
    href=models.URLField()
    title=models.TextField()
    nasa_id=models.CharField(max_length=100)
    media_type=models.CharField(max_length=100)
    center=models.CharField(max_length=300)
    keywords=models.TextField()
    description_508=models.CharField(max_length=100)
    secondary_creator=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    album=models.TextField()
    photographer=models.CharField(max_length=100)
    preview=models.URLField()
    orig=models.URLField()
    def __str__(self):
        return self.title
class MetaResult(models.Model):
    total_hits=models.IntegerField()
    href=models.URLField()


