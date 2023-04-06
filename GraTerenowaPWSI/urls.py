"""GraTerenowaPWSI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from gra import views

app_name = 'gra'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:ses_id>/', views.room, name='room'),
    path('get_new/', views.newses, name='newses'),
    #path('<int:ses_id>/game/add_score/', views.room, name='name'),
    path('test_photo', views.test_photo, name='test_photo'),
]