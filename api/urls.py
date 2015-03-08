from django.conf.urls import patterns, url
from views import ReviewCreateView, ReviewDetailView, ReviewUpdateView, ReviewDeleteView

urlpatterns = patterns('',
                       url(r'^add/$', ReviewCreateView.as_view(), name='create'),
                       url(r'^(?P<pk>[\w\d]+)/$', ReviewDetailView.as_view(), name='detail'),
                       url(r'^(?P<pk>[\w\d]+)/edit/$', ReviewUpdateView.as_view(), name='update'),
                       url(r'^(?P<pk>[\w\d]+)/delete/$', ReviewDeleteView.as_view(), name='delete'),
)