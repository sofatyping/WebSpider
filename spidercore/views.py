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
		root_url = crawling_url

		if "http" not in crawling_url and "https" not in crawling_url:
			crawling_url = "http://" + crawling_url + "/"

		try:
			response = urllib2.urlopen(crawling_url)
			html_content = response.read()
		except:
			return render_to_response('homepage.html',
                {'canopen': False,},context_instance=RequestContext(request))

		layer=1
		level=0
		if crawling_layer.isdigit():
			layer = int(crawling_layer)

		temp_set = [crawling_url]
		res = {}
		iterate_layer = []

		soup = BeautifulSoup(html_content)
		hyperlink = soup.findAll('a')
		childrenlsit = []

		for tag in hyperlink:
			if "https" in tag['href'] or "http" in tag['href']:
				if tag['href'] not in temp_set:
					if url in tag['href']:
						childrenlsit.append(tag['href'])
						temp_set.append(tag['href'])
			else if url in tag['href']:
				temp_url = "http://"+tag['href']+"/"
				if temp_url not in temp_set:
					childrenlsit.append(tag['temp_url'])
					temp_set.append(temp_url)

		iterate_layer.append(childrenlsit)
		res[crawling_url] = childrenlsit

		while level<layer:
			# temp_content = temp_queue.popleft()
			childrenlsit = []
			
			for collection in iterate_layer[level]:
				try:
					response = urllib2.urlopen(collection)
					temp_content = response.read()
				except:
					continue

				soup = BeautifulSoup(temp_content)
				hyperlink = soup.findAll('a')
				for tag in hyperlink:
					if "https" in tag['href'] or "http" in tag['href']:
						if tag['href'] not in temp_set:
							if url in tag['href']:
								childrenlsit.append(tag['href'])
								temp_set.append(tag['href'])
					else if url in tag['href']:
						temp_url = "http://"+tag['href']+"/"
						if temp_url not in temp_set:
							childrenlsit.append(tag['temp_url'])
							temp_set.append(temp_url)
				res[collection] = childrenlsit
			level = level + 1

			if childrenlsit:
				iterate_layer.append(childrenlsit)
			else:
				break


		return HttpResponseRedirect("/")
	else:
		return HttpResponseRedirect("/")
