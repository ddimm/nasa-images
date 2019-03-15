from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.utils.http import urlencode
from .forms import ImageSearch
from .models import ImageResult, MetaResult
from urllib import request
import json
from django.core.paginator import Paginator
import django.contrib.sessions


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
                kwargs[key]=kwargs.get(key).replace(" ", "%20")
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
                elif key=="year_start" and type(kwargs[key])==str:
                    if kwargs[key]=='None':
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
        meta=MetaResult(**x.get("collection").get("metadata"),href=x.get("collection").get("href"))#obtain the meta data, i.e. total number of this and link to data
        for outer in x.get("collection").get("items"):
            for tag in outer.get("data"):
                orig=None
                if(tag.get("media_type")=="image"):
                    try:
                        orig=json.load(request.urlopen(outer.get("href")))[0]
                    except Exception as e:
                        results.append(ImageResult(**tag, href=outer.get("href"), preview=outer.get("links")[0].get("href"),orig=None))
                    results.append(ImageResult(**tag, href=outer.get("href"), preview=outer.get("links")[0].get("href"),orig=orig)) #only append images, because that's what we want
        return results, meta
        
       

    



# Create your views here.
def home(request):
    return render(request, 'main/home.html', {"form":ImageSearch()})
def getSearch(request):
    
    if(request.method=="POST"):
        form=ImageSearch(request.POST)
        request.session['search']=request.POST
        if form.is_valid():
            data_set, meta=getData(**form.cleaned_data, media_type="image")
            
            paginator=Paginator(data_set, 5)
            page=request.GET.get('page')
            data=paginator.get_page(page)
            
            cont=urlencode(form.cleaned_data)
            return render(request, "main/result.html", {"results":data, "meta": meta, "form":ImageSearch(initial=form.cleaned_data),"cont":cont})
        else:
            form = ImageSearch()
            return render(request, "main/search.html", {"form": form})
    elif not request.method=="POST":
        
        path=request.GET.dict()
        del path['page']
       
        data_set, meta=getData(**path, media_type="image")
        paginator=Paginator(data_set, 5)
        page=request.GET.get('page')
        data=paginator.get_page(page)
        cont=dict()
        cont=urlencode(path)
        return render(request, "main/result.html", {"results":data, "meta": meta, "form":ImageSearch(initial=path),"cont":cont})


    return render(request, "main/search.html", {"form": ImageSearch()})
def help(request):
    return render(request,"main/help.html", {"form":ImageSearch()})



