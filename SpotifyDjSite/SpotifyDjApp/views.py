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



def topArtists():
        cid = 'ee9fc019f133485296b33e83b6e674f9'
        secret = '519f3c8ab9e646a5bdc484a6a643b2aa'

        sp_auth = oauth2.SpotifyOAuth(
                client_id = cid,
                client_secret = secret,
                redirect_uri = "http://127.0.0.1:8008/SpotifyDjApp/spotify_callback",
                scope = 'user-top-read'
        )

        redirect_url = sp_auth.get_authorize_url()
        auth_token = sp_auth.get_access_token()  
        #print(auth_token['access_token'])

        if auth_token:
                sp = spotipy.Spotify(auth=auth_token['access_token'])
                results = sp.current_user_top_artists(limit=10,offset=0,time_range='medium_term')
                #print(results)
                listTest = []
                for i in range(10):
                        listTest.append(results['items'][i]['name'])
                return listTest
        else:
                return "error"