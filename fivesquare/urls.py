from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from api.views import ReviewListView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fivesquare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', ReviewListView.as_view(), name='list'),
    url(r'^post/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)



