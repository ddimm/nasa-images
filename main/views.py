from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.utils.http import urlencode
from .forms import ImageSearch
from .models import ImageResult, MetaResult, Search
from urllib import request
import json
from django.core.paginator import Paginator
from random import randint

def form_to_model(form):
    vals_to_add=dict()
    
    for key in form.keys():
        if form.get(key)==None:
            vals_to_add[key]=0
        else:
            vals_to_add[key]=form.get(key)
    Search(**vals_to_add).save()
            


NASA_URL="https://images-api.nasa.gov/search?"
def getData(**kwargs): #obtain the results from the information from the form
    results=[]
    meta=None
    if len(kwargs)==0:
        return results.append(ImageResult(description="None"))#if there are no results
    else:
        url=[]
        url.append(NASA_URL)
        #go through each tag and encode it so it's url friendly
        for key in kwargs:
            if key=="search":
                kwargs[key]=kwargs.get(key).replace(" ", "%20")
                url.append("q")
                url.append("=")
                url.append(kwargs[key])
                url.append("&")  
                continue
            elif kwargs[key]!=None or kwargs[key]!="": #all this may be overkill, but urlencode may not give the url needed
                if type(kwargs[key])==int:
                    url.append(key)
                    url.append("=")
                    url.append(str(kwargs[key]))
                    url.append("&")
                    continue
                elif key=="year_start" and type(kwargs[key])==str:
                    if kwargs[key]=='None': #if they form is none, we get 'None' in the string the next time
                        continue
                    else:
                        url.append(key)
                        url.append("=")
                        url.append(kwargs[key])
                        url.append("&")
                elif key=="year_end" and type(kwargs[key])==str:
                    if kwargs[key]=="None":
                        continue
                    else:
                        url.append(key)
                        url.append("=")
                        url.append(kwargs[key])
                        url.append("&")
                elif type(kwargs[key])==str and kwargs[key]!="":
                    kwargs[key]=kwargs.get(key).replace(" ", "%20")
                    url.append(key)
                    url.append("=")
                    url.append(kwargs[key])
                    url.append("&")
                    continue
        page=request.urlopen("".join(url))
        x=json.load(page)
        for outer in x.get("collection").get("items"):
            for tag in outer.get("data"):
                orig=None #declare orig here so its scope can be used elsewhere
                if(tag.get("media_type")=="image"):
                    try:
                        orig=json.load(request.urlopen(outer.get("href")))[0]
                    except Exception as _:
                        results.append(ImageResult(**tag, href=outer.get("href"), preview=outer.get("links")[0].get("href"),orig=None))
                    results.append(ImageResult(**tag, href=outer.get("href"), preview=outer.get("links")[0].get("href"),orig=orig)) #only append images, because that's what we want
        meta=MetaResult(total_hits=len(results),href=x.get("collection").get("href"))#obtain the meta data, i.e. total number of this and link to data
        #meta.save()
        return results, meta
        
# Create your views here.
def home(request):
    return render(request, 'main/home.html', {"form":ImageSearch()})
def getSearch(request):
    #handles the post request from the form, and subsequent get requests after
    if(request.method=="POST"):#for the form post
        form=ImageSearch(request.POST)
        if form.is_valid():
            #Search(**form.cleaned_data).save()
            
           # form_to_model(form.cleaned_data)
            data_set, meta=getData(**form.cleaned_data, media_type="image")#get the data from the form
            paginator=Paginator(data_set, 5)
            page=request.GET.get('page')
            data=paginator.get_page(page)#get the paginator
            
            cont=urlencode(form.cleaned_data)#url for pages
            return render(request, "main/result.html", {"results":data, "meta": meta, "form":ImageSearch(initial=form.cleaned_data),"cont":cont})
        else:
            form = ImageSearch()
            return render(request, "main/search.html", {"form": form})
    elif not request.method=="POST":
        
        path=request.GET.dict()
        if 'page' in path:#check to see if the page variable there. this prevents an error from doing something like home/search
            del path['page'] #get rid of the page variable since we don't need it anymore
            data_set, meta=getData(**path, media_type="image")
            paginator=Paginator(data_set, 5)
            page=request.GET.get('page')
            data=paginator.get_page(page)
            cont=dict()
            cont=urlencode(path)
            return render(request, "main/result.html", {"results":data, "meta": meta, "form":ImageSearch(initial=path),"cont":cont})
        else:
            return render(request, "main/search.html", {"form": ImageSearch()})
    return render(request, "main/search.html", {"form": ImageSearch()})    
def help(request):
    #for the help page
    return render(request,"main/help.html", {"form":ImageSearch()})



