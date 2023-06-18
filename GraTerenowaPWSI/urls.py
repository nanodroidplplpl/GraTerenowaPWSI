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
from django.contrib import admin

from gra import views

app_name = 'gra'
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.index, name='index'),
    path('', views.game_index, name='game_index'),
    path('<int:ses_id>/', views.room, name='room'),
    path('zaslepka/', views.zaslepka, name='zaslepka'),
    path('choose_group/', views.choose_group, name='choose_gorup'),
    path('group_screen/', views.group_screen, name='group_screen'),
    path('game_filed/', views.game_filed, name='game_filed'),
    path('host_game_create/', views.host_game_create, name='host_game_create'),
    path('game_creation/', views.game_creation, name='game_creation'),
    path('host_game_filed/', views.host_game_filed, name='host_game_filed'),
    path('group_screen/<int:ekipy_id>/', views.group_screen, name='group_screen'),
    # path('get_new/', views.newses, name='newses'),
    # path('<int:ses_id>/game/add_score/', views.room, name='name'),
    # path('test_photo', views.test_photo, name='test_photo'),
    path('create_session/', views.newses, name='newses'),
    path('create_session/creator/<int:ses_id>', views.creator_room, name='creator_room')
]
