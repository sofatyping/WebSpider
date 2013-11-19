# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib2
import os

DEFAULT_LAYER = 1

def startcrawl(request):
	return render_to_response('homepage.html',
                {},context_instance=RequestContext(request))

def crawling(request):
	if request.method == "POST":

		crawling_url = request.POST.get("crawlurl").strip()
		crawling_layer = request.POST.get("crawllevel").strip()
		root_url = crawling_url

		if "http" not in crawling_url and "https" not in crawling_url:
			crawling_url = "http://" + crawling_url

		try:
			response = urllib2.urlopen(crawling_url)
			html_content = response.read()
		except:
			return render_to_response('Homepage.html',
                {'canopen': False,},context_instance=RequestContext(request))

		layer=DEFAULT_LAYER
		level=0
		if crawling_layer.isdigit():
			layer = int(crawling_layer)

		temp_set = [crawling_url]
		res = {}
		iterate_layer = {}
		childrenlist = []
		error_dict={}

		getsubhyperlink(crawling_url, html_content, childrenlist, temp_set)
		iterate_layer[level] = childrenlist
		res[crawling_url] = childrenlist

		while level<layer:
			childrenlist = []
			
			for collection in iterate_layer[level]:
				try:
					response = urllib2.urlopen(collection)
					temp_content = response.read().encode('utf8')
				except:
					continue

				errors = seoanalysis(temp_content)
				error_dict[collection]=errors
				getsubhyperlink(crawling_url, temp_content, childrenlist, temp_set)
				res[collection] = childrenlist

			level = level + 1

			if childrenlist:
				iterate_layer[level]=childrenlist
			else:
				break
		
		print iterate_layer
		print "$$$$$$$$$$-$"
		print error_dict
		return render_to_response('Result.html',
                {"result":res, "layer":iterate_layer,"error_list":error_dict,},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/")

def about(request):
	return render_to_response('About.html',
                {},context_instance=RequestContext(request))


def getsubhyperlink(origin_url, html_content, reslist, temp_set):
	soup = BeautifulSoup(html_content, parseOnlyThese=SoupStrainer('a'))
	hyperlink = soup.findAll('a',href=True)

	for tag in hyperlink:
		if "https" in tag['href'] or "http" in tag['href']:
			if tag['href'] not in temp_set:
				if origin_url in tag['href']:
					reslist.append(tag['href'])
					temp_set.append(tag['href'])
		else:
			if "www" in tag['href']:
				temp_url = "http://"+tag['href']
				if temp_url not in temp_set:
					if origin_url in temp_url:
						reslist.append(temp_url)
						temp_set.append(temp_url)
			else:
				if tag['href'] and tag['href'][0] == '/': 
					temp_url = origin_url + tag['href']
					if temp_url not in temp_set:
						reslist.append(temp_url)
						temp_set.append(temp_url)
				else:
					temp_url = origin_url + tag['href']
					if temp_url not in temp_set:
						reslist.append(temp_url)
						temp_set.append(temp_url)

def get_body_text(html_text):
    soup = BeautifulSoup(html_text)
    hyperlink = soup.findAll('a',href=True,Text=True)
    return unicode(hyperlink)

def seoanalysis(html_content):
	print "abc"
	soup = BeautifulSoup(html_content)
	cssstyle = soup.findAll(style=True)
	error_list = []

	for css in cssstyle:
		if "#" in css or ":" in css:
			error_list.append("CSS Style should stand alone from HTML page.")
			break

	script = soup.findAll('script')

	for js in script:
		if "document" in js or "ready" in js or "function" in js:
			error_list.append("Javascript files should stand alone from HTML page.")
			break

	image = soup.findAll('img')
	images = soup.findAll('img', alt=True)
	if not len(image) == len(images):
		error_list.append("Every image should have alt attribute.")

	for photo in image:
		filetype = photo['src']
		fileName, fileExtension = os.path.splitext(filetype)
		if "png" not in fileExtension:
			error_list.append("Use PNG image is loading faster.")
			break

	metadata = soup.findAll('meta')
	if len(metadata)<3:
		error_list.append("Web page is lack of keywords.")
	if len(metadata)>10:
		error_list.append("There are too many keywords in the web page.")

	if "h1" not in html_content or "h2" not in html_content or "h3" not in html_content or "h4" not in html_content:
		error_list.append("It would better use h1,h2,h3 tag to classify content.")

	if "strong" not in html_content:
		error_list.append("It would better use strong tag to emphasize content.")

	if "table" in html_content:
		error_list.append("It would better use div tag rather than table tag.")

	if "title" not in html_content:
		error_list.append("It would better add a title tag into web page.")

	# first_div = soup.find('div')
	# second_div = first_div.find('div')
	# third_div = second_div.find('div')
	# div_list = third_div.find('div')
	# if len(div_list) >0:
	
	# error_list.append("The number of div layer should less than 3.")
	return error_list

