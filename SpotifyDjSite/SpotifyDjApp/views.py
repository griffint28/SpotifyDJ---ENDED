from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.core.mail import send_mail as send_email
from django.http import JsonResponse
from django.conf import settings
from .models import *

def index(request):
        return render(request=request, template_name= "../templates/SpotifyDjApp/homepage.html")
# Create your views here.

#SpotifyDjSite/SpotifyDjApp/templates/SpotifyDjApp/homepage.html