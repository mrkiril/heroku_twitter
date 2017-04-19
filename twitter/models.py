from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Twitter(models.Model):

    class Meta():
        db_table = "twitter"
    twitter_user = models.ForeignKey(
        User, 
        unique=False, 
        verbose_name="twitter_user")
    twitter_text = models.TextField('twitter_text')
    twitter_date = models.DateTimeField('twitter_date')

    
 





