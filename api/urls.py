from django.conf.urls import patterns, url

from views import StoreCreateView, StoreDetailView, StoreUpdateView, StoreDeleteView, ReviewCreateView, \
    ReviewDetailView, ReviewUpdateView, ReviewDeleteView


urlpatterns = patterns('',
                       # url(r'^all/$', StoreListView.as_view(), name='list'),
                       url(r'^add/$', StoreCreateView.as_view(), name='create'),
                       url(r'^(?P<pk>[\w\d]+)/$', StoreDetailView.as_view(), name='detail'),
                       url(r'^edit/(?P<pk>[\w\d]+)/$', StoreUpdateView.as_view(), name='update'),
                       url(r'^delete/(?P<pk>[\w\d]+)/$', StoreDeleteView.as_view(), name='delete'),
                       url(r'^add/review/$', ReviewCreateView.as_view(), name='review_create'),
                       url(r'^review/(?P<pk>[\w\d]+)/$', ReviewDetailView.as_view(), name='review_detail'),
                       url(r'^review/edit/(?P<pk>[\w\d]+)/$', ReviewUpdateView.as_view(), name='review_update'),
                       url(r'^review/delete/(?P<pk>[\w\d]+)/$', ReviewDeleteView.as_view(), name='review_delete'),
)