from django.conf.urls import patterns, url

from views import StoreCreateView, StoreDetailView, StoreUpdateView, StoreDeleteView, ReviewCreateView, \
    ReviewDetailView, ReviewUpdateView, ReviewDeleteView


urlpatterns = patterns('',
                       url(r'^add/store/$', StoreCreateView.as_view(), name='create'),
                       url(r'^store/(?P<pk>[\w\d]+)/$', StoreDetailView.as_view(), name='detail'),
                       url(r'^store/(?P<pk>[\w\d]+)/edit/$', StoreUpdateView.as_view(), name='update'),
                       url(r'^store/(?P<pk>[\w\d]+)/delete/$', StoreDeleteView.as_view(), name='delete'),
                       url(r'^add/review/$', ReviewCreateView.as_view(), name='review_create'),
                       url(r'^review/(?P<pk>[\w\d]+)/$', ReviewDetailView.as_view(), name='review_detail'),
                       url(r'^review/(?P<pk>[\w\d]+)/edit/$', ReviewUpdateView.as_view(), name='review_update'),
                       url(r'^review/(?P<pk>[\w\d]+)/delete/$', ReviewDeleteView.as_view(), name='review_delete'),
)