from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
from os import getenv
from django.middleware.csrf import get_token as generate_csrf
# Create your views here.

# Render homepage with posts from DB:
def renderHomepage(request):
   now = datetime.now()
   posts = UserPost.objects.all();

   c = RequestContext(request, {'post_list':posts})
   return render_to_response('home.html', c)


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

def authenticate(request):
   
   # Create an initial facebook authentication redirect url, a la 
   # https://developers.facebook.com/docs/authentication/server-side/
   facebookurl = 'https://www.facebook.com/dialog/oauth?'
   
   # Add the facebook app ID, stored in an environment variable
   facebookurl += 'client_id='
   facebookurl += getenv('FUTURE_FB_KEY')
   
   # Add a redirect url, which must be the same as one indicated in
   # the fb app settings
   facebookurl += '&redirect_uri='
   facebookurl += urlencode('http://localhost:5000/facebookauth')
   
   # don't think we need additional permissions for now, but if we do,
   # later can uncomment these lines. see 
   # https://developers.facebook.com/docs/authentication/permissions/
   #facebookurl += '&scope='
   #facebookurl += COMMA_SEPARATED_LIST_OF_PERMISSION_NAMES
   
   # To protect against CSRF, add a key which is then checked later
   facebookurl += '&state='
   csrf_key = generate_csrf()
   facebookurl += csrf_key

