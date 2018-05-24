# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Mobikedata
from .GPSTransform import GPSUtil
from django.http import JsonResponse


# Create your views here.
def mobindex(request):
    return render(request,'mobike/mobindex.html')
def index(request):
    return render(request,'mobike/index.html')

def test(request):
    return render(request,'mobike/indextest.html')

def reqpath(request):
    try:
        startTime=request.GET['startTime']
    except:
        startTime=r'2017-10-01 07:00:00.0'
    gtools=GPSUtil()
    mobikelines=Mobikedata.objects.filter(starttime__startswith=startTime[0:13])[0:1000]
    mb=[]
    for m in mobikelines:
        pathpoints=[x.split(',') for s in m.pathstr[1:].split('#') for x in s.split(';')[:-1]]
        coords=[]
        for p in pathpoints:
            p[0]=float(p[0])
            p[1]=float(p[1])
            if p[0]>0 and p[1]>0:
                bd=gtools.wgs2bd(p[1],p[0])
                #print bd
                coords.append([bd['lon'],bd['lat']])
        if len(coords)>1:
            mb.append(coords)
    return JsonResponse({'mobikelines':mb})