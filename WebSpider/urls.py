from django.conf.urls import patterns, include, url

from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    url(r'^home/$', home, name='home'),
    url(r'^channel/$', channel, name='channel'),
    url(r'^$', index, name='index'),
    url(r'^test/$', test, name='test'),
    )


