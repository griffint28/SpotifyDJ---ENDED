from django.shortcuts import render
from django.shortcuts import *
import django
from .functions import topSongsID
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
        cid = 'ee9fc019f133485296b33e83b6e674f9'
        secret = '519f3c8ab9e646a5bdc484a6a643b2aa'

        AUTH_URL = 'https://accounts.spotify.com/api/token'

        # POST
        auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': cid,
        'client_secret': secret,
        })

        # convert the response to JSON
        auth_response_data = auth_response.json()

        # save the access token
        access_token = auth_response_data['access_token']

        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        BASE_URL = 'https://api.spotify.com/v1/'

        topSongsDance =[]
        topSongsEnergy = []
        topSongsLoudness = []
        topSongsAcousticness = []
        songIdList = topSongsID()
        for songId in songIdList:
                track_id = songId
                r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
                r = r.json()      
                topSongsDance.append(r["danceability"])
                topSongsEnergy.append(r["energy"])
                topSongsLoudness.append(r["loudness"])
                topSongsAcousticness.append(r["acousticness"])

        return render(request, "../templates/SpotifyDjApp/topsongs.html", {"list":topSongsAcousticness})

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
        userTopSongs = topSongs()
        cid = 'ee9fc019f133485296b33e83b6e674f9'
        secret = '519f3c8ab9e646a5bdc484a6a643b2aa'

        AUTH_URL = 'https://accounts.spotify.com/api/token'

        auth_response = requests.post(AUTH_URL, {
                'grant_type': 'client_credentials',
                'client_id': cid,
                'client_secret': secret,
        })

        auth_response_data = auth_response.json()

        # save the access token
        access_token = auth_response_data['access_token']

        headers = {
                'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        listTest = []
        idTest = []
        for song in userTopSongs:
                infoSplit = song.split("-")
                limit = '?limit=3'
                market = "&market=US"
                seed_artists = "&seed_artists="+infoSplit[0]
                seed_genres = "&seed_genres=indie"
                seed_tracks = "&seed_tracks="+infoSplit[1]
                BASE_URL = 'https://api.spotify.com/v1/'

                #r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
                r = requests.get(BASE_URL + 'recommendations/' +
                        limit + market + seed_artists + seed_genres + seed_tracks, headers=headers)
                
                r = r.json()
                #print(r)

                
                for i in range(3):
                        listTest.append(r['tracks'][i]['name'] + " - " + r['tracks'][i]['artists'][0]['name'] + "\n")
                        #idTest.append(r['tracks'][i]['id'])
        return render(request, "../templates/SpotifyDjApp/suggestedLost.html", {"list":listTest})


def topSongs():
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
                results = sp.current_user_top_tracks(limit=10,offset=0,time_range='medium_term')
                #print(results)
                listTest = []
                for i in range(10):
                        listTest.append(results['items'][i]['name'] + " - " + results['items'][i]['artists'][0]['name'] + "\n")
                        #listTest.append(results['items'][i]['artists'][0]['id'] + "-" + results['items'][i]['id'])
                return listTest
        else:
                return "error"


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