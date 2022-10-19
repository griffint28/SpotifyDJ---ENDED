from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='hompage'),
    path('login', views.login, name='login'),
    path('list', views.list, name='list'),
    path('spotifytest', views.spotifytest, name='spotifytest'),
    path('spotifyplayer', views.spotifyplayer, name='spotifyplayer'),
    path('test', views.test, name='test'),

]