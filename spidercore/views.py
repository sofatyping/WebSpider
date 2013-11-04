# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from BeautifulSoup import BeautifulSoup
import urllib2

def startcrawl(request):
	return render_to_response('homepage.html',
                {},context_instance=RequestContext(request))

def crawling(request):
	if request.method == "POST":

		crawling_url = request.POST.get("crawlurl").strip()
		crawling_layer = request.POST.get("crawllevel").strip()

		if "http" not in crawling_url and "https" not in crawling_url:
			crawling_url = "http://" + crawling_url + "/"

		try:
			response = urllib2.urlopen(crawling_url)
			html_content = response.read()
		except:
			return render_to_response('homepage.html',
                {'canopen': False,},context_instance=RequestContext(request))

		soup = BeautifulSoup(html_content)
		# TODO: BST or DST
		
		return HttpResponseRedirect("/")
	else:
		return HttpResponseRedirect("/")