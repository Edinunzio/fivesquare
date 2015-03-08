from django.conf.urls import patterns, url

from views import ReviewCreateView, StoreDetailView, ReviewUpdateView, ReviewDeleteView


urlpatterns = patterns('',
                       url(r'^add/$', ReviewCreateView.as_view(), name='create'),
                       url(r'^(?P<pk>[\w\d]+)/$', StoreDetailView.as_view(), name='detail'),
                       url(r'^(?P<pk>[\w\d]+)/edit/$', ReviewUpdateView.as_view(), name='update'),
                       url(r'^(?P<pk>[\w\d]+)/delete/$', ReviewDeleteView.as_view(), name='delete'),
)