from django.conf.urls import patterns, include, url

from django.contrib import admin


urlpatterns = patterns('spidercore.views',
    # Examples:
    url(r'^$', 'startcrawl'),
    url(r'^crawling/?$', 'crawling'),
	# url(r'^results/?$', 'crawling'),
	url(r'^about/?$', 'about'),
    )


