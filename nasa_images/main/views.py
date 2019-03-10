from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ImageSearch
from .models import ImageResult, MetaResult
from urllib import request
import json

NASA_URL="https://images-api.nasa.gov/search?"
def getData(**kwargs):
    results=[]
    meta=None
    if len(kwargs)==0:
        return results.append(ImageResult(description="None"))
    else:
        url=[]
        url.append(NASA_URL)
        
        for key in kwargs:
            if key=="search":
                kwargs[key]=kwargs.get(key).replace(" ", "%")
                url.append("q")
                url.append("=")
                url.append(kwargs[key])
                url.append("&")  
                continue
            elif kwargs[key]!=None or kwargs[key]!="":
                if type(kwargs[key])==int:
                    url.append(key)
                    url.append("=")
                    url.append(str(kwargs[key]))
                    url.append("&")
                    continue
                elif type(kwargs[key])==str and kwargs[key]!="":
                    kwargs[key]=kwargs.get(key).replace(" ", "%")
                    
                    url.append(key)
                    url.append("=")
                    url.append(kwargs[key])
                    url.append("&")
                    continue
        
       
        page=request.urlopen("".join(url))
        x=json.load(page)
        meta=MetaResult(**x.get("collection").get("metadata"),href=x.get("collection").get("href"))#obtain the meta data, i.e. total number of this and link to data
        for outer in x.get("collection").get("items"):
            for tag in outer.get("data"):
                
                if(tag.get("media_type")=="image"):
                    results.append(ImageResult(**tag)) #only append images, because that's what we want
        return results, meta
        
       

    



# Create your views here.
def home(request):
    return render(request, 'main/head.html')
def getSearch(request):
    if(request.method=="POST"):
        form=ImageSearch(request.POST)
        if form.is_valid():
            data, meta=getData(**form.cleaned_data)
            return render(request, "main/result.html", {"results":data, "meta": meta})
        else:
            form = ImageSearch()
        return render(request, "main/search.html", {"form": form})
    else:
        return render(request, "main/search.html", {"form": ImageSearch()})

