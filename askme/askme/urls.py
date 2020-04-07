"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('hot/', views.hot_view, name='hot'),
    # path('settings/', views.settings_view, name='settings'),
    # path('login/', views.login_view, name='login'),
    # path('singup/', views.signup_view, name='singup'),
    # path('ask/', views.ask_view, name='ask'),
    # path('question/<int:pk>', views.questions_view, name='question'),
    # path('tag/<slug:slug>', views.tags_view, name='tag')
]