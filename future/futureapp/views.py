from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import *
from fandjango.decorators import facebook_authorization_required

# Create your views here.

# Render homepage with posts from DB:
@facebook_authorization_required
def renderHomepage(request):
   now = datetime.now()
   return render_to_response('future/testhome.html', {'current_date':now})



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

        


