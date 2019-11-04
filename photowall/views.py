from django.shortcuts import render,HttpResponse
from django.views import generic
from .models import Photos


def imageListView(request):
        datas=Photos.objects.filter(isshow=True)
        return render(request,'index.html',locals())
