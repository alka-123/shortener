from django.shortcuts import render_to_response, get_object_or_404, render
import random, string, json
from shortener.models import Urls
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template.context_processors import csrf
 
def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('shortener/index.html', c)
 
def redirect_original(request, short_id):
    url = get_object_or_404(Urls, pk=short_id) # get object, if not found return 404 error
    url.count += 1
    url.save()
    return HttpResponseRedirect(url.httpurl)
 
def shorten_url(request):
    url = request.POST.get("url", '')
    if not (url == ''):
        short_id = get_short_code()
        b = Urls(httpurl=url, short_id=short_id)
        b.save()
 
        response_data = {}
        response_data['url'] = settings.SITE_URL + "/" + short_id
        return HttpResponse(json.dumps(response_data),  content_type="application/json")
    return HttpResponse(json.dumps({"error": "error occurs"}), content_type="application/json")
 
def get_short_code():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Urls.objects.get(pk=short_id)
        except:
            return short_id




#index : It opens the index page by rendering the template.
#redirect_original : It redirects short URL to it�s original URL.
#shorten_url : We will make a request to this view to create and return us the short URL.
#get_short_code : This will generate the unique short code/id for URLs.
