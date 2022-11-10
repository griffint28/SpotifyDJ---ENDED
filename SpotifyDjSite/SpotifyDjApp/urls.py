from django.urls import path
from . import views

urlpatterns = [
    #landing page
    path('', views.homepage, name='homepage'),

    #blank login page
    path('login', views.login, name='login'), 
    
    #blank account registration page
    path('register', views.register, name='register'),

    #testing list returns (for dev)
    path('list', views.list, name='list'),

    #testing of spotify authenication (for dev)
    path('spotifytest', views.spotifytest, name='spotifytest'),

    #testing of spotify player (for dev)
    path('spotifyplayer', views.spotifyplayer, name='spotifyplayer'),

    #top songs for user, with each page being a different timeframe
    #s for short_term, m for medium_term, and l for long_term
    path('topsongs', views.topsongs, name='topsongs'),
    path('topsongsm', views.topsongsm, name='topsongsm'),
    path('topsongsl', views.topsongsl, name='topsongsl'),

    #top artist for user, no changable timeframe
    path('topartists', views.topartists, name='topartists'),

    #top 10 short_term songs suggestions 
    path('suggestions', views.suggestions, name='suggestions'),

    #search page (in work)
    path('search', views.search, name='search'),

    #features for ajax (account registration, login, saving song, and search)
    path('registerPost', views.registerPost, name='registerPost'),
    path('loginGet', views.loginGet, name='loginGet'),
    path('saveSong', views.saveSong, name='saveSong'),
    path('doSearch', views.doSearch, name='doSearch')


]