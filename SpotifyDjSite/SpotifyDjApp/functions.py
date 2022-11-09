from django.shortcuts import render
from django.shortcuts import *
from .models import *
from spotipy import Spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import oauth2
import requests
from datetime import date
import json



def topSongsID(timeframe = 'short_term'):
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
            results = sp.current_user_top_tracks(limit=10,offset=0,time_range=timeframe)
            #print(results)
            listTest = []
            for i in range(10):
                    listTest.append(results['items'][i]['id'])
            return listTest
    else:
            return "error"

def topSongsArtistsId(timeframe = 'short_term'):
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
            results = sp.current_user_top_tracks(limit=10,offset=0,time_range=timeframe)
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

def topSongs(timeframe = 'short_term'):
        cid = 'ee9fc019f133485296b33e83b6e674f9'
        secret = '519f3c8ab9e646a5bdc484a6a643b2aa'

        sp_auth = oauth2.SpotifyOAuth(
                client_id = cid,
                client_secret = secret,
                redirect_uri = "http://127.0.0.1:8008/SpotifyDjApp/spotify_callback",
                scope = 'user-top-read, user-library-modify'
        )

        redirect_url = sp_auth.get_authorize_url()
        auth_token = sp_auth.get_access_token()  
        #print(auth_token['access_token'])

        if auth_token:
                sp = spotipy.Spotify(auth=auth_token['access_token'])
                results = sp.current_user_top_tracks(limit=10,offset=0,time_range=timeframe)
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
                #print(r['tracks'][0])
                recommendations.append(r['tracks'][0]['id'])
        
        return recommendations

def topArtists(timeframe= 'short_term'):
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
                results = sp.current_user_top_artists(limit=10,offset=0,time_range=timeframe)
                #print(results)
                listTest = []
                for i in range(10):
                        listTest.append(results['items'][i]['name'])
                return listTest
        else:
                return "error"

def getSongNameArtist(songID):     
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
        r = requests.get(BASE_URL + 'tracks/' + songID, headers=headers)
        r = r.json()
        songAndArtists = r['name'] + " - " + r['album']['artists'][0]['name']

        return songAndArtists

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

def saveSongSpotify(songID, usernameIn):
        cid = 'ee9fc019f133485296b33e83b6e674f9'
        secret = '519f3c8ab9e646a5bdc484a6a643b2aa'

        sp_auth = oauth2.SpotifyOAuth(
                client_id = cid,
                client_secret = secret,
                redirect_uri = "http://127.0.0.1:8008/SpotifyDjApp/spotify_callback",
                scope = 'user-top-read, user-library-modify'
        )

        redirect_url = sp_auth.get_authorize_url()
        auth_token = sp_auth.get_access_token()  

        if auth_token:
                sp = spotipy.Spotify(auth=auth_token['access_token'])
                songs = []
                songs.append(songID)
                results = sp.current_user_saved_tracks_add(tracks=songs)
                if (not(checkIfEntryInUserSugg(usernameIn))):
                        result = userSuggestions.objects.create(
                                username = usernameIn,
                                posFeedback = {"Song ID" : songID},
                                negFeedback = {"Bad Song ID" : ""},
                                dateCaptured = date.today()
                        )
                else:
                        user = userSuggestions.objects.filter(username__icontains=usernameIn).first()
                        if user is None:
                                return "error"
                        else:
                                oldSongIdSql = user.posFeedback["Song ID"]
                                newSongIdSql = str(oldSongIdSql + ", " + songID)
                                user = userSuggestions.objects.filter(username__icontains=usernameIn).first()
                                user.posFeedback = {"Song ID" : newSongIdSql}  
                                user.dateCaptured = date.today()                       
                                user.save()
                                return "saved"

                return "saved"
        else:
                return "error"

def checkIfEntryInUserSugg(username):
        userExist = userSuggestions.objects.filter(username__icontains=username).first()
        if userExist is None:
                return False
        else:
                return True