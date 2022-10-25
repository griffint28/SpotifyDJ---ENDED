from django.shortcuts import render
from django.shortcuts import *
import django
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

def topSongsID():
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
                    listTest.append(results['items'][i]['id'])
            return listTest
    else:
            return "error"
