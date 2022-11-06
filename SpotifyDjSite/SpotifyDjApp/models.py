from django.db import models

# Create your models here.
class userInfo(models.Model):
    username = models.CharField(max_length=100) 
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class userToken(models.Model):
    username = models.CharField(max_length=100) 
    aceess_token = models.CharField(max_length=150) 
    expiration_period = models.CharField(max_length=100) 
    refresh_token = models.CharField(max_length=150) 
 
class userStats(models.Model):
    username = models.CharField(max_length=100) 
    topSongs = models.JSONField()
    topArtists = models.JSONField()
    dateCaptured = models.DateTimeField() 
  
class userSuggestions(models.Model):
    username = models.CharField(max_length=100) 
    posFeedback = models.JSONField()
    negFeedback = models.JSONField()
    dateCaptured = models.DateTimeField()