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
    path('test', views.test, name='test'),
   

]

urlpatterns += staticfiles_urlpatterns()