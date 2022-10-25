from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='hompage'),
    path('login', views.login, name='login'),
    path('list', views.list, name='list'),
    path('spotifytest', views.spotifytest, name='spotifytest'),
    path('spotifyplayer', views.spotifyplayer, name='spotifyplayer'),
    path('suggestions', views.suggestions, name='suggestions'),
    path('register', views.register, name='register'),
    path('topsongs', views.topsongs, name='topsongs'),
    path('topartists', views.topartists, name='topartists'),

    path('post/ajax/registerPost', views.registerPost, name='registerPost'),


]