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
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .models import userInfo
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json



def homepage(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/home.html")

def login(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/Login.html")

def topsongs(request):
        value = request.COOKIES.get("username")
        if value is None:
                print("error")
        else:
                print("username in top songs is " + value)

        list = topSongs('short_term')
        listId= topSongsID('short_term')
        listDance = []
        listEnergy = []
        listAcoustic = []
        listLoudness = []
        listCompiled = {}
        
        for song in listId:
                topSongStats = songStats(song)
                listDance.append(topSongStats["danceability"])
                listEnergy.append(topSongStats["energy"])
                listAcoustic.append(topSongStats["acousticness"])
                listLoudness.append(topSongStats["loudness"])
        listCompiled['songs'] = list
        listCompiled['dance'] = listDance
        listCompiled['energy'] = listEnergy
        listCompiled['acoustic'] = listAcoustic
        listCompiled['loud'] = listLoudness
        return render(request, "../templates/SpotifyDjApp/topsongs.html", {"list":listCompiled})

def topsongsm(request):
        list = topSongs('medium_term')
        listId= topSongsID('medium_term')
        listDance = []
        listEnergy = []
        listAcoustic = []
        listLoudness = []
        listCompiled = {}
        
        for song in listId:
                topSongStats = songStats(song)
                listDance.append(topSongStats["danceability"])
                listEnergy.append(topSongStats["energy"])
                listAcoustic.append(topSongStats["acousticness"])
                listLoudness.append(topSongStats["loudness"])
        listCompiled['songs'] = list
        listCompiled['dance'] = listDance
        listCompiled['energy'] = listEnergy
        listCompiled['acoustic'] = listAcoustic
        listCompiled['loud'] = listLoudness
        return render(request, "../templates/SpotifyDjApp/topsongs.html", {"list":listCompiled})

def topsongsl(request):
        list = topSongs(timeframe = 'long_term')
        listId= topSongsID(timeframe = 'long_term')
        listDance = []
        listEnergy = []
        listAcoustic = []
        listLoudness = []
        listCompiled = {}
        
        for song in listId:
                topSongStats = songStats(song)
                listDance.append(topSongStats["danceability"])
                listEnergy.append(topSongStats["energy"])
                listAcoustic.append(topSongStats["acousticness"])
                listLoudness.append(topSongStats["loudness"])
        listCompiled['songs'] = list
        listCompiled['dance'] = listDance
        listCompiled['energy'] = listEnergy
        listCompiled['acoustic'] = listAcoustic
        listCompiled['loud'] = listLoudness
        return render(request, "../templates/SpotifyDjApp/topsongs.html", {"list":listCompiled})

def register(request):
        return render(request, "../templates/SpotifyDjApp/register.html")

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
        listRecommendationsID = recommendations(listTopSongs, listTopSongsID, listTopSongsArtistsID, listGenre)
        dictRecommendations = {}
        for songID in listRecommendationsID:
                dictRecommendations[songID] = (getSongNameArtist(songID))
        return render(request, "../templates/SpotifyDjApp/suggestedList.html", {"dictRec":dictRecommendations})

def registerPost(request):
        request_data = request.body
        request_dict = json.loads(request_data.decode('utf-8'))
        credentials = request_dict.get("credentials")

        obj = userInfo.objects.filter(username__icontains=credentials.get("username")).first()
        if obj is not None:
                result = 1
        else:
                user = userInfo.objects.create(
                        username=credentials.get("username"),
                        first_name=credentials.get("fname"),
                        last_name=credentials.get("lname"),
                        email=credentials.get("email"),
                        password=credentials.get("password")
                )
                # authenticate will return a user object if successful ...
                if user is not None:
                # user is successfully authenticated
                # auth_login(request, user)
                        result = 0
                else:
                # this should never be the case
                        result = 2

                # if error happens make sure we catch that gracefully
                # if there is a problem return either success or fail
        return JsonResponse({"message": result})

def loginGet(request):
        result = 1
        # get the payload from the ajax call
        request_data = request.body

        # get the json dictionary from the body
        request_dict = json.loads(request_data.decode('utf-8'))

        info = request_dict.get("credentials")
        usernameIn = info.get("username")
        passwordIn = info.get("password")
        try: 
                obj = userInfo.objects.filter(username__icontains=usernameIn).first()
                if obj is None:
                        result = 1
                        return JsonResponse({"message": result})
                else:
                        if ((obj.password).strip() == passwordIn.strip()):
                                result = 0
                                response = JsonResponse({"message": result})
                                response.set_cookie(key="username", value=obj.username)
                                return response
                        else:
                                result = 1
                                return JsonResponse({"message":result})
        except:
                result = 2
                return JsonResponse({"message": result})
        
def saveSong(request):
        try:    
                username = request.COOKIES.get("username")
                request_data = request.body
                request_dict = json.loads(request_data.decode('utf-8'))
                songID = request_dict.get("songInfo")
                answer = saveSongSpotify(songID, username)
                print(answer)
                if answer == "saved":
                        result =  0
                        return JsonResponse({"message": result})
                else:
                        result =  1
                        return JsonResponse({"message": result})  
        except:
                result = 1
                return JsonResponse({"message": result})

