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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from rest_framework_swagger.views import get_swagger_view

from app import views, rest_views

schema_view = get_swagger_view(title='Askme')

urlpatterns = [
    url('', include('django_prometheus.urls')),
    path('django-admin/', admin.site.urls),
    # Legacy API
    path('api/v1/', views.index_view, name='index'),
    path('api/v1/hot/', views.hot_view, name='hot'),
    path('api/v1/settings/', views.settings_view, name='settings'),
    path('api/v1/login/', views.login_view, name='login'),
    path('api/v1/logout/', views.logout_view, name='logout'),
    path('api/v1/signup/', views.signup_view, name='signup'),
    path('api/v1/ask/', views.ask_view, name='ask'),
    path('api/v1/question/<int:pk>/', views.questions_view, name='question'),
    path('api/v1/tag/<slug:slug>/', views.tags_view, name='tag'),
    path('api/v1/vote/', views.vote_view, name='vote'),
    path('api/v1/question/<int:pk>/answer/', views.answer_view, name='answer'),
    # REST API
    url('api/v2/swagger/', schema_view),
    path('api/v2/questions', rest_views.index_view, name='new'),
    path('api/v2/questions/hot', rest_views.hot_view, name='rest_hot'),
    path('api/v2/questions/<int:qid>', rest_views.question_id_view, name='one_question'),
    path('api/v2/questions/<int:qid>/answers', rest_views.question_answer_view, name='rest_answer'),
    path('api/v2/users', rest_views.users_view, name='users'),
    path('api/v2/users/<int:uid>', rest_views.user_id_view, name='one_user'),
    path('api/v2/settings', rest_views.settings_view, name='rest_settings'),
    path('api/v2/tags', rest_views.tags_view, name='tags'),
    path('api/v2/tags/<slug:slug>', rest_views.question_tag_view, name='by_tag'),
    path('api/v2/signup', rest_views.signup_view, name='rest_signup'),
    path('api/v2/login', rest_views.login_view, name='rest_login'),
    path('api/v2/logout', rest_views.logout_view, name='rest_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
