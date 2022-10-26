from django.shortcuts import render
from django.shortcuts import *
from .models import *
from spotipy import Spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import oauth2
import requests



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



def topSongsArtistsId():
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
                    listTest.append(results['items'][i]['artists'][0]['id'])
            return listTest
    else:
            return "error"


def topSongsGenre():
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

        topSongsGenre =[]
        songIdList = topSongsArtistsId()
        for songId in songIdList:
                artist_id = songId
                r = requests.get(BASE_URL + 'artists/' + artist_id, headers=headers)
                r = r.json()      
                if(len(r["genres"]) == 0):
                        topSongsGenre.append("pop")
                else:
                        topSongsGenre.append(r["genres"][0])
        return topSongsGenre



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

def recommendations(listTopSongs, listTopSongsID, listTopSongsArtistsID, listGenre):
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

        recommendations = []
        for i in range(len(listTopSongs)):              
                limit = '?limit=1'
                market = "&market=US"
                seed_artists = "&seed_artists=" + listTopSongsArtistsID[i]
                seed_genres = "&seed_genres=" + listGenre[i]
                seed_tracks = "&seed_tracks=" + listTopSongsID[i]
                BASE_URL = 'https://api.spotify.com/v1/'
                r = requests.get(BASE_URL + 'recommendations/' +
                        limit + market + seed_artists + seed_genres + seed_tracks, headers=headers)
                r = r.json()
                recommendations.append(r['tracks'][0]['name'] + " - " + r['tracks'][0]['artists'][0]['name'])

        
        return recommendations

        

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

def songStats(songId):
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

        r = requests.get(BASE_URL + 'audio-features/' + songId, headers=headers)
        return (r.json())