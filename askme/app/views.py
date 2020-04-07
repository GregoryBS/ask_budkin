from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404


def index_view(request):
    return render('src/index.html')


def hot_view(request):
    return render('src/index.html')
