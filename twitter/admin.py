from django.contrib import admin
from twitter.models import Twitter
# Register your models here.


class TwitterAdmin(admin.ModelAdmin):
    fields = [
        'twitter_user',
        'twitter_text',
        'twitter_date'
    ]
    list_filter = ['twitter_date']
    list_display = ('twitter_user', 'twitter_date', 'twitter_text')

# Register your models here.
admin.site.register(Twitter, TwitterAdmin)
