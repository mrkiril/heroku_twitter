from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
#import twitter.views
from twitter import views
from django.conf import settings
from django.conf.urls.static import static

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    #url(r'^$', hello.views.index, name='index'),
    #url(r'^db', hello.views.db, name='db'),
    #url(r'^test', hello.views.test, name='test'),
    #url(r'^admin/', include(admin.site.urls)),

    url(r'^admin/', admin.site.urls),
    url(r'^reg/', views.registration),
    url(r'^auth/', views.authentefication),
    url(r'^logout/', views.logout),
    url(r'^blog/', views.blog),
    url(r'^twit/', include('twitter.urls')),
    url(r'^static/.*', views.static),
    url(r'^lalka/', views.lalka),
]
