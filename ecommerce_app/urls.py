from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard),
    path('cop', views.cop),
    path('flip', views.flip),
    path('discuss', views.discuss),
    path('shoebox', views.shoebox),
    path('myshoebox', views.myshoebox),
    path('upload_shoe', views.upload),
    path('delete/<int:shoe_id>', views.delete),
    path('like/<int:shoe_id>', views.like),
    path('sell_shoe', views.sell),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout)
]