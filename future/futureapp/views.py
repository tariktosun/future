from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *

# Create your views here.

# Render homepage with posts from DB:
def renderHomepage(request):
   now = datetime.now()
   p = UserPost.objects.get(text="THETESTPOST")
   c = RequestContext(request, {'current_date':now, 'title': p.title, 'text':
           p.text})
   return render_to_response('future/testhome.html', c)


# make a post.
def post(request):
    if request.method == 'POST':
        newPost = UserPost(title = 'foo', #title=request.POST['title'],
                     text = request.POST['text'],
                     #author = request.session['userid'],
        #             tags = (),
        #             mentions = ()
                          )
        newPost.save()
        return HttpResponse(newPost.text)
    else:
        return HttpResponse('SOMETHING IS WRONG.')

        


