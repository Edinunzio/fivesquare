from django.conf.urls import patterns, include, url
from django.contrib import admin

from api.views import StoreListView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fivesquare.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', StoreListView.as_view(), name='list'),
    url(r'^store/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)



