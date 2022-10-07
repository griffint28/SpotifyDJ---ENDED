from django.shortcuts import render
from django.shortcuts import *
from .models import *
from spotipy import Spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import oauth2
import requests


def homepage(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/homepage.html")

def login(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/Login.html")

def list(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/list.html")

def spotifytest2(request):
        base_url = 'https://api.spotify.com/v1/'
        client_id = 'ee9fc019f133485296b33e83b6e674f9'
        client_secret = '519f3c8ab9e646a5bdc484a6a643b2aa'
        auth_url = 'https://accounts.spotify.com/api/token'
        data = {
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret,
        }

        auth_response = requests.post(auth_url, data=data)

        access_token = auth_response.json().get('access_token')

        if access_token:
                headers = {
                        'Authorization': 'Bearer {}'.format(access_token)
                }

                return HttpResponse("text")
        else:
                print("error")
                return render(request=request, template_name= "../templates/SpotifyDjApp/spotifytest.html")


def spotifytest(request):
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
        print(auth_token['access_token'])

        if auth_token:
                sp = spotipy.Spotify(auth=auth_token['access_token'])
                results = sp.current_user_top_tracks(limit=50,offset=0,time_range='medium_term')
                listTest = []
                for i in range(50):
                        listTest.append(results['items'][i]['name'] + " - " + results['items'][i]['album']['artists'][0]['name'] + "\n")
                return HttpResponse(listTest)
        else:
                return render(request=request, template_name= "../templates/SpotifyDjApp/spotifytest.html")

