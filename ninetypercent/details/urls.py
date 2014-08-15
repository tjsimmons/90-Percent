from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'details.views.home', name='home'),
    url(r'^details/(?P<debtornum>\d*)/$', 'details.views.details', name='details'),
    url(r'^search/$', 'details.views.search', name='search'),
)
