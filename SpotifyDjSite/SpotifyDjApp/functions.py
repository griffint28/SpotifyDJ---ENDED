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

#cid and secret are values obtained from creating a project 
#in spotify dashboard. It allows access to spotify api and is
#needed for all forms of spotify authenication

#functions that have to access a user's personal information
#use spotipy. Spotipy is python library of spotify's API
#General functions (no personal info) are used with
#Spotify's API by using requests (GET, POST, etc)

#LONG TERM WANT FOR THIS FILE:
#create a function (or two if needed), that removes duplicate code
#of setting auth in all of the functions belows       

#changable timeframe, deafults to short term 
def topSongsID(timeframe = 'short_term'):
    #set authenication 
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

    #if token exists 
    if auth_token:
            #using spotipy, obtain top songs
            sp = spotipy.Spotify(auth=auth_token['access_token'])
            results = sp.current_user_top_tracks(limit=10,offset=0,time_range=timeframe)
            listTest = []
            #then get the id of the top songs
            for i in range(10):
                    listTest.append(results['items'][i]['id'])
            return listTest
    else:
            return "error"

#changable timeframe, deafults to short term 
def topSongsArtistsId(timeframe = 'short_term'):
    #set authenication 
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
        
    #if token exists 
    if auth_token:
            #using spotipy obtain the artists id of the top songs     
            sp = spotipy.Spotify(auth=auth_token['access_token'])
            results = sp.current_user_top_tracks(limit=10,offset=0,time_range=timeframe)
            #return list of artists id of the user's top songs
            listTest = []
            for i in range(10):
                    listTest.append(results['items'][i]['artists'][0]['id'])
            return listTest
    else:
            return "error"

def topSongsGenre():
        #set authenication (no personal info needed)
        cid = 'ee9fc019f133485296b33e83b6e674f9'
        secret = '519f3c8ab9e646a5bdc484a6a643b2aa'
        AUTH_URL = 'https://accounts.spotify.com/api/token'
        auth_response = requests.post(AUTH_URL, {
                'grant_type': 'client_credentials',
                'client_id': cid,
                'client_secret': secret,
        })
        auth_response_data = auth_response.json()

        #setting url for request to spotify's api
        access_token = auth_response_data['access_token']
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        BASE_URL = 'https://api.spotify.com/v1/'

        #setting empty list to be used
        topSongsGenre =[]
        #get top songs again to find ids of the songs
        songIdList = topSongsArtistsId()
        for songId in songIdList:
                #for each song, garb the song id and append ot list
                artist_id = songId
                r = requests.get(BASE_URL + 'artists/' + artist_id, headers=headers)
                r = r.json()      
                #if there is no genre for the artist, then append a general genre, "pop"
                if(len(r["genres"]) == 0):
                        topSongsGenre.append("pop")
                else:
                        #append genre of artist 
                        topSongsGenre.append(r["genres"][0])
        return topSongsGenre

#changable timeframe, deafults to short term 
def topSongs(timeframe = 'short_term'):
        #set authenicaiton
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

        #if token exists
        if auth_token:
                #using spotipy, get users top songs
                sp = spotipy.Spotify(auth=auth_token['access_token'])
                results = sp.current_user_top_tracks(limit=10,offset=0,time_range=timeframe)
                list = []
                #get songs names and artist name 
                for i in range(10):
                        list.append(results['items'][i]['name'] + " - " + results['items'][i]['artists'][0]['name'] + "\n")
                return list
        else:
                return "error"

def recommendations(listTopSongs, listTopSongsID, listTopSongsArtistsID, listGenre):
        #input:
        #listTopSongs - Song names are needed for url of spotify API
        #listTopSongsID - Song IDs are needed for url of spotify API
        #listTopSongsArtistsID - Artists names are needed for url of spotify API
        #listGenre - Genre is needed for url of spotify API
        
        #set authenication
        cid = 'ee9fc019f133485296b33e83b6e674f9'
        secret = '519f3c8ab9e646a5bdc484a6a643b2aa'
        AUTH_URL = 'https://accounts.spotify.com/api/token'
        auth_response = requests.post(AUTH_URL, {
                'grant_type': 'client_credentials',
                'client_id': cid,
                'client_secret': secret,
        })
        auth_response_data = auth_response.json()

        #setting url for spotify's api
        access_token = auth_response_data['access_token']
        headers = {
                'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        #setting blank list of song ids for recommendations
        list = {}
        recommendations = []
        recIDs = []
        for i in range(len(listTopSongs)):  
                #extra info for setting url that might have variable changes            
                limit = '?limit=1'
                market = "&market=US"
                seed_artists = "&seed_artists=" + listTopSongsArtistsID[i]
                seed_genres = "&seed_genres=" + listGenre[i]
                seed_tracks = "&seed_tracks=" + listTopSongsID[i]
                BASE_URL = 'https://api.spotify.com/v1/'
                
                #for each song in top songs, get one recommendation  
                r = requests.get(BASE_URL + 'recommendations/' +
                        limit + market + seed_artists + seed_genres + seed_tracks, headers=headers)
                r = r.json()
                
                #append the id of recommended songs 
                #appends id to display iframe
                recommendations.append(r['tracks'][0]['name'] + " - " + r['tracks'][0]['artists'][0]['name'])
                recIDs.append(r['tracks'][0]['id'])
                list['recommendations'] = recommendations
                list['ID'] = recIDs
        
        return list
        
        return recommendations

#changable timeframe, deafults to short term 
def topArtists(timeframe= 'short_term'):
        #set authenication
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

        #if token exists
        if auth_token:
                #using spotipy, get users top artist (no correlation to songs)
                sp = spotipy.Spotify(auth=auth_token['access_token'])
                results = sp.current_user_top_artists(limit=10,offset=0,time_range=timeframe)
                #append the names of artists to return
                list = {}
                artist = []
                id =[]
                for i in range(10):
                        artist.append(results['items'][i]['name'])
                        id.append(results['items'][i]['id'])
                list['artist'] = artist
                list['ID'] = id
                return list
        else:
                return "error"

def getSongNameArtist(songID):
        #set authenication     
        cid = 'ee9fc019f133485296b33e83b6e674f9'
        secret = '519f3c8ab9e646a5bdc484a6a643b2aa'
        AUTH_URL = 'https://accounts.spotify.com/api/token'
        auth_response = requests.post(AUTH_URL, {
                'grant_type': 'client_credentials',
                'client_id': cid,
                'client_secret': secret,
        })
        auth_response_data = auth_response.json()

        #setting url for request to spotify's apiting 
        access_token = auth_response_data['access_token']
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        BASE_URL = 'https://api.spotify.com/v1/'

        #for the one songId, send the request with the proper info
        r = requests.get(BASE_URL + 'tracks/' + songID, headers=headers)
        r = r.json()

        #set a strign with the song name and artist name
        songAndArtists = r['name'] + " - " + r['album']['artists'][0]['name']

        return songAndArtists

def songStats(songId):
        #set authenication
        cid = 'ee9fc019f133485296b33e83b6e674f9'
        secret = '519f3c8ab9e646a5bdc484a6a643b2aa'
        AUTH_URL = 'https://accounts.spotify.com/api/token'
        auth_response = requests.post(AUTH_URL, {
                'grant_type': 'client_credentials',
                'client_id': cid,
                'client_secret': secret,
        })
        auth_response_data = auth_response.json()

        #setting url for request to spotify's api
        access_token = auth_response_data['access_token']
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        BASE_URL = 'https://api.spotify.com/v1/'

        #send request for info of song anayltics for one song
        r = requests.get(BASE_URL + 'audio-features/' + songId, headers=headers)

        #return all data of audio feature
        return (r.json())

def saveSongSpotify(songID, usernameIn):
        #set authenication
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

        #if token exists
        if auth_token:
                #using spotipy
                sp = spotipy.Spotify(auth=auth_token['access_token'])
                songs = []
                songs.append(songID)
                #add to user's liked song based on the song ID
                results = sp.current_user_saved_tracks_add(tracks=songs)
                #check if SpotifyDJ user entry exists in table
                if (not(checkIfEntryInUserSugg(usernameIn))):
                        #if there is no entry for the user in the table
                        #create a new entry
                        result = userSuggestions.objects.create(
                                username = usernameIn,
                                posFeedback = {"Song ID" : songID},
                                negFeedback = {"Bad Song ID" : ""},
                                dateCaptured = date.today()
                        )
                else:
                        #if the SpotifyDJ user has an entry in the table, then modify
                        user = userSuggestions.objects.filter(username__icontains=usernameIn).first()
                        if user is None:
                                #error checking
                                return "error"
                        else:
                                #obtain old entry, modify, then add back and save 
                                oldSongIdSql = user.posFeedback["Song ID"]
                                newSongIdSql = str(oldSongIdSql + ", " + songID)
                                user = userSuggestions.objects.filter(username__icontains=usernameIn).first()
                                user.posFeedback = {"Song ID" : newSongIdSql}  
                                user.dateCaptured = date.today()                       
                                user.save()
                                return "saved"
                #return if sucessful
                return "saved"
        else:
                return "error"

def checkIfEntryInUserSugg(username):
        #function to check if there is an entry based on 
        #the SpotifyDJ username in the table of userSuggestions
        userExist = userSuggestions.objects.filter(username__icontains=username).first()
        if userExist is None:
                #returns that there is no entry for that user
                return False
        else:
                #returns that is an entry for that user
                return True

def doSearchEng(songIn, artistIn):
        #
        # W O R K - I N - P R O G R E S S
        #
        # Successful: 
        # Auth works, and getting feedback from spotify api
        #
        # Problems: 
        # Spotify doesn't return up to limit 
        #       |___(limit is set to 10, but might return 3 or 6 or 9. Inconsisent, depending on search)
        # What type of format to return so it shows in page
        # Allowing rerun if search results is inaccurate 
        #


        #set authenication
        cid = 'ee9fc019f133485296b33e83b6e674f9'
        secret = '519f3c8ab9e646a5bdc484a6a643b2aa'
        AUTH_URL = 'https://accounts.spotify.com/api/token'
        auth_response = requests.post(AUTH_URL, {
                'grant_type': 'client_credentials',
                'client_id': cid,
                'client_secret': secret,
        })
        auth_response_data = auth_response.json()

        #setting url for request to spotify's api
        access_token = auth_response_data['access_token']
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        BASE_URL = 'https://api.spotify.com/v1/'
        limit = 'limit=10'


        songIn.replace(" ", '%20')
        artistIn.replace(" ", "%20")
        r = requests.get(BASE_URL + 'search?query=remaster%2520track%3A' + songIn + '%2520artist%3AB' + artistIn + '&type=track&market=US&locale=en-US%2Cen%3Bq%3D0.9&offset=5&limit=10', headers=headers)
        
        return(r.json())

