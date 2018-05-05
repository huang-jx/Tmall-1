from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def get_head_data(request):
    return


# 前后端分离,返回的时候不是模板 而是json数据
def get_search_shop(request):
    keywords = request.GET.get('key')



    return HttpResponse('',)
