from django.urls import path

from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('homepage', views.homepage, name='hompage'),
    path('login', views.login, name='login'),
    path('list', views.list, name='list'),
    path('spotifytest', views.spotifytest, name='spotifytest'),
<<<<<<< HEAD
    path('spotifyplayer', views.spotifyplayer, name='spotifyplayer'),
    path('test', views.test, name='test'),
=======
    path('test', views.test, name='test'),
   
>>>>>>> 382f95cff9d11f9e8fde0a6ec545d5656a9b8c42

]

urlpatterns += staticfiles_urlpatterns()