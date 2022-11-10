from django.shortcuts import render
from django.shortcuts import *
from .functions import *
from .models import *
from spotipy import Spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import oauth2
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .models import userInfo
from django.http import JsonResponse
from django.http import HttpResponse
import json



def homepage(request):
        #returns landing page, no input
        #deletes any cookies to reset
        response = render(request=request, template_name= "../templates/SpotifyDjApp/home.html")
        for cookie in request.COOKIES:
                response.delete_cookie(cookie)
        return response

def login(request):
        #returns blank login page with form, takes no input
        return render(request=request, template_name= "../templates/SpotifyDjApp/Login.html")

def topsongs(request):
        #get SpotifyDJ username through cookies
        value = request.COOKIES.get("username")
        #obtain short songs and their ids
        list = topSongs('short_term')
        listId= topSongsID('short_term')
        #blank lists for analytics of songs 
        listDance = []
        listEnergy = []
        listAcoustic = []
        listLoudness = []
        listCompiled = {}       
        #for each song in the top songs 
        #(limited to 10 in topSongs and topSongsID functions)
        for song in listId:
                #grab analytics for each songs, and append to correlating list
                topSongStats = songStats(song)
                listDance.append(topSongStats["danceability"])
                listEnergy.append(topSongStats["energy"])
                listAcoustic.append(topSongStats["acousticness"])
                listLoudness.append(topSongStats["loudness"])
        #complie lists as dict, and return to page included in the json 
        listCompiled['songs'] = list
        listCompiled['dance'] = listDance
        listCompiled['energy'] = listEnergy
        listCompiled['acoustic'] = listAcoustic
        listCompiled['loud'] = listLoudness
        #return and display page, with json containing top song info
        return render(request, "../templates/SpotifyDjApp/topsongs.html", {"list":listCompiled})

def topsongsm(request):
        #obtain medium_term songs and their ids
        list = topSongs('medium_term')
        listId= topSongsID('medium_term')
        #blank lists for analytics of songs
        listDance = []
        listEnergy = []
        listAcoustic = []
        listLoudness = []
        listCompiled = {}
        #for each song in the top songs 
        #(limited to 10 in topSongs and topSongsID functions)
        for song in listId:
                #grab analytics for each songs, and append to correlating list
                topSongStats = songStats(song)
                listDance.append(topSongStats["danceability"])
                listEnergy.append(topSongStats["energy"])
                listAcoustic.append(topSongStats["acousticness"])
                listLoudness.append(topSongStats["loudness"])
        #complie lists as dict, and return to page included in the json 
        listCompiled['songs'] = list
        listCompiled['dance'] = listDance
        listCompiled['energy'] = listEnergy
        listCompiled['acoustic'] = listAcoustic
        listCompiled['loud'] = listLoudness
        #return and display page, with json containing top song info
        return render(request, "../templates/SpotifyDjApp/topsongs.html", {"list":listCompiled})

def topsongsl(request):
        #obtain long_term songs and their ids
        list = topSongs(timeframe = 'long_term')
        listId= topSongsID(timeframe = 'long_term')
        #blank lists for analytics of songs
        listDance = []
        listEnergy = []
        listAcoustic = []
        listLoudness = []
        listCompiled = {}
        #for each song in the top songs 
        #(limited to 10 in topSongs and topSongsID functions)
        for song in listId:
                #grab analytics for each songs, and append to correlating list
                topSongStats = songStats(song)
                listDance.append(topSongStats["danceability"])
                listEnergy.append(topSongStats["energy"])
                listAcoustic.append(topSongStats["acousticness"])
                listLoudness.append(topSongStats["loudness"])
        #complie lists as dict, and return to page included in the json 
        listCompiled['songs'] = list
        listCompiled['dance'] = listDance
        listCompiled['energy'] = listEnergy
        listCompiled['acoustic'] = listAcoustic
        listCompiled['loud'] = listLoudness
        #return and display page, with json containing top song info
        return render(request, "../templates/SpotifyDjApp/topsongs.html", {"list":listCompiled})

def register(request):
        #returns blank registration page, no input needed
        return render(request, "../templates/SpotifyDjApp/register.html")

def list(request):
        #test page for testing if list were obtained through spotify
        #page can be deleted, no dependencies 
        return render(request=request, template_name= "../templates/SpotifyDjApp/list.html")

def spotifytest(request):
        #test page for testing connection between project and spotify
        #page can be deleted, no dependencies 
        return HttpResponse(topSongs())

def topartists(request):
        #no input
        #obtains list of top artists for user
        list = topArtists()
        #returns top artist page and the list of top artist
        return render(request, "../templates/SpotifyDjApp/topArtists.html", {"list":list})

def spotifyplayer(request):
        ##test page for testing connection between project and spotify web player
        #page can be deleted, no dependencies 
        return render(request=request, template_name= "../templates/SpotifyDjApp/spotifyplayer.html")

def suggestions(request):
        #obtain top songs for user
        listTopSongs = topSongs()
        #obtain the correlating id of top songs for user
        listTopSongsID = topSongsID()
        #obtain the correlating artist id of top songs for user
        listTopSongsArtistsID = topSongsArtistsId()
        #obtain the correlating genre of top songs for user
        listGenre = topSongsGenre()
        #generate recommendations, and a list of song ids is returned from Spotify API
        listRecommendationsID = recommendations(listTopSongs, listTopSongsID, listTopSongsArtistsID, listGenre)
        #blank dict for parsing song recommendation list
        dictRecommendations = {}
        #for each song in song recommendation
        #(limited to 10, in every function referenced above)
        for songID in listRecommendationsID:
                #get the song name and artist name for each songID obtained from recommendation list
                dictRecommendations[songID] = (getSongNameArtist(songID))
        #return suggestions page, with json containing the name and artist of recommendations 
        #(song ids of recommendation were not returned as not needed in page)
        return render(request, "../templates/SpotifyDjApp/suggestedList.html", {"dictRec":dictRecommendations})

def registerPost(request):
        #obtain input from ajax that contains account creation ifo
        request_data = request.body
        request_dict = json.loads(request_data.decode('utf-8'))
        credentials = request_dict.get("credentials")
        #check if username already exists in our database
        obj = userInfo.objects.filter(username__icontains=credentials.get("username")).first()
        #if obj is not none, that means a username is taken and need new input
        if obj is not None:
                #1 is returned to signal in javascript new input is needed
                result = 1
        else:
                #username is not taken, therefore, create user
                user = userInfo.objects.create(
                        username=credentials.get("username"),
                        first_name=credentials.get("fname"),
                        last_name=credentials.get("lname"),
                        email=credentials.get("email"),
                        password=credentials.get("password")
                )
                if user is not None:
                        #user is not none when account is successfuly created and stored
                        #return 0 for success and set cookies
                        result = 0
                        response = JsonResponse({"message": result})
                        response.set_cookie(key="username", value=user.username)
                        return response
                else:
                        #user creation error, return bad error 
                        result = 2

        #return if successful, error, or username taken
        return JsonResponse({"message": result})

def loginGet(request):
        #obtain input to check valid login
        request_data = request.body
        request_dict = json.loads(request_data.decode('utf-8'))
        info = request_dict.get("credentials")

        #variables ending with 'In', is input that needs to be checked
        usernameIn = info.get("username")
        passwordIn = info.get("password")
        try: 
                #check if username exists in user database, if so, user is returned
                obj = userInfo.objects.filter(username__icontains=usernameIn).first()
                #if obj is none, no user with that username exist
                if obj is None:
                        #return 1 for invalid login
                        result = 1
                        return JsonResponse({"message": result})
                else:
                        #check user's password with input password
                        if ((obj.password).strip() == passwordIn.strip()):
                                #valid and returns succesful login and set cookies
                                result = 0
                                response = JsonResponse({"message": result})
                                response.set_cookie(key="username", value=obj.username)
                                return response
                        else:
                                #return 1 for invalid login
                                result = 1
                                return JsonResponse({"message":result})
        except:
                #return 2 for unexpected error
                result = 2
                return JsonResponse({"message": result})
        
def saveSong(request):
        try:    
                #obtain username through cookie to save action to our database
                username = request.COOKIES.get("username")
                #obtain input of song id that user wants to save to their spotify
                request_data = request.body
                request_dict = json.loads(request_data.decode('utf-8'))
                songID = request_dict.get("songInfo")
                #funciton to save song to spotify and our database
                answer = saveSongSpotify(songID, username)
                #if answer is anything except 'saved', error
                if answer == "saved":
                        #answer is saved and is successful in all actions
                        result =  0
                        return JsonResponse({"message": result})
                else:
                        #return error
                        result =  1
                        return JsonResponse({"message": result})  
        except:
                #return error at any point
                result = 1
                return JsonResponse({"message": result})

def search(request):
        #return blank search page
         return render(request, "../templates/SpotifyDjApp/search.html") 

def doSearch(request):
        #
        # W O R K - I N - P R O G R E S S
        #
        # Successful: 
        # Auth works, and getting feedback from spotify api
        #
        # Problems: 
        # Spotify doesn't return up to limit 
        #       |___(limit is set to 10, but might return 3 or 6 or 9. Inconsisent, depending on search)
        # What type of format to return so it shows in page?
        # Allowing rerun if search results is inaccurate? 
        #


        #obtain input of song name and artist name
        #for now, artist name is required but might be optional later after fully functional
        request_data = request.body
        request_dict = json.loads(request_data.decode('utf-8'))
        searchIn = request_dict.get("searchIn")
        songIn = searchIn.get("songIn")
        artistIn = searchIn.get("artistIn")

        #preform search with spotify's search api 
        searchResults = doSearchEng(songIn, artistIn)



        #I want to return all of json, so song Id, name and artist is all accessible 
        #for other features after this one (recommendations based on selection)
        #But problems with returning search results to display

        #Possibly solutions:
        #Pass search resutls to new page as "searchResults.html" instead of trying to keep it one page
        #Parse to where it only returns information I want to keep (slim down amount of info)
        #return json as a single string and then JSON parse in javascript (works best so far, but JSON.parse is not working, making it hard to get info out of)
        #Maybe HttpResponse instead of Json? But ajax expects value to tell if sucessful or not

        response = {}
        #a for loop is NEEDED as amount of search results is inconsisent
        for i in range(len(searchResults['tracks']['items'])):
                dictIndex = "index" + str(i)
                response[dictIndex] = searchResults['tracks']['items'][i]['name']
        return JsonResponse({"message": str(response)})
