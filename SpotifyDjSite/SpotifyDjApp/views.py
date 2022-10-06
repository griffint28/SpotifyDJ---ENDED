from django.shortcuts import render
from django.shortcuts import *
from .models import *

def homepage(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/homepage.html")

def login(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/Login.html")

def list(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/list.html")

def spotifytest(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/spotifytest.html")

#SpotifyDjSite/SpotifyDjApp/templates/SpotifyDjApp/homepage.html