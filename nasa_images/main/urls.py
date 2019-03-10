
from django.urls import path
from django.urls import re_path
from . import views

appName='main'

urlpatterns=[
    path("", views.home, name="home"),
    path("search/",views.getSearch,name="search"),
    path("search.html", views.getSearch, name="search"),
    re_path(r'home', views.home, name="home"),
    re_path(r'search', views.getSearch, name="search"),
    
    
]