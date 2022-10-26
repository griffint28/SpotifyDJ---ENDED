from django.shortcuts import render
from django.shortcuts import *
import django
from .functions import *
from .models import *
from spotipy import Spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import oauth2
import requests
from .forms import userForm
from .models import user
from django.http import JsonResponse
from django.core import serializers



def homepage(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/home.html")

def login(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/Login.html")

def topsongs(request):
        list = topSongs()
        listId= topSongsID()
        listDance = []
        listEnergy = []
        listAcoustic = []
        listTempo = []
        for song in listId:
                topSongStats = songStats(song)
                listDance.append(topSongStats["danceability"])
                listEnergy.append(topSongStats["energy"])
                listAcoustic.append(topSongStats["acousticness"])
                listTempo.append(topSongStats["tempo"])

        return render(request, "../templates/SpotifyDjApp/topsongs.html", {"list":list})

def register(request):
        form = userForm()
        friends = user.objects.all()
        return render(request, "../templates/SpotifyDjApp/register.html",  {"form": form, "user": user})

def registerPost(request):
        print("Im here")
        if request.is_ajax and request.method == "POST":
                # get the form data
                form = userForm(request.POST)
                # save the data and after fetch the object in instance
                if form.is_valid():
                        instance = form.save()
                # serialize in new friend object in json
                ser_instance = serializers.serialize('json', [ instance, ])
                 # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

def list(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/list.html")

def spotifytest(request):
        return HttpResponse(topSongs())

def topartists(request):
        list = topArtists()
        return render(request, "../templates/SpotifyDjApp/topArtists.html", {"list":list})

def spotifyplayer(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/spotifyplayer.html")

def suggestions(request):
        listTopSongs = topSongs()
        listTopSongsID = topSongsID()
        listTopSongsArtistsID = topSongsArtistsId()
        listGenre = topSongsGenre()
        listRecommendations = recommendations(listTopSongs, listTopSongsID, listTopSongsArtistsID, listGenre)
        return render(request, "../templates/SpotifyDjApp/suggestedList.html", {"list":listRecommendations})

