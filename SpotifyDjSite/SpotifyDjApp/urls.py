from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login', views.login, name='login'),
    path('list', views.list, name='list'),
    path('spotifytest', views.spotifytest, name='spotifytest'),
    path('spotifyplayer', views.spotifyplayer, name='spotifyplayer'),
    path('register', views.register, name='register'),

    path('topsongs', views.topsongs, name='topsongs'),
    path('topsongsm', views.topsongsm, name='topsongsm'),
    path('topsongsl', views.topsongsl, name='topsongsl'),

    path('topartists', views.topartists, name='topartists'),
    path('suggestions', views.suggestions, name='suggestions'),

    path('registerPost', views.registerPost, name='registerPost'),
    path('loginGet', views.loginGet, name='loginGet'),
    path('saveSong', views.saveSong, name='saveSong'),




]