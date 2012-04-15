from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from urllib import quote
from models import *
from os import getenv
from django.conf import settings
from string import letters,digits,join
from random import choice
import requests
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

def fbauth(request):
   # The url for this page, to be passed as a param to facebook for redirection
   facebookredirect = settings.BASE_URI + 'fbauth/'
   facebookredirect = quote(facebookredirect, '')
   
   # if the incoming request is a redirect from facebook with a code
   # that may be exchanged for an oauth token
   if request.method == 'GET':
      if request.GET.get('code', '') != '' and request.session['fb_csrf']:
         # Check that the request has a valid csrf token that matches
         # the one stored in the session
         if request.session['fb_csrf'] == request.GET.get('state', ''):
            
            # Create a url to exchange the code received for an oauth token
            oauthurl = 'https://graph.facebook.com/oauth/access_token?'
            
            # Add the fb app ID
            oauthurl += 'client_id='
            oauthurl += settings.FACEBOOK_APP_ID
            
            # Add a redirect url, which should point back to this page
            oauthurl += '&redirect_uri='
            oauthurl += facebookredirect

            # Add our app's secret, from developer.facebook.com
            oauthurl += '&client_secret='
            oauthurl += settings.FACEBOOK_API_SECRET

            oauthurl += '&code='
            oauthurl += request.GET['code']
            
            gettoken = requests.get(oauthurl)
            return HttpResponse(gettoken.text)
      
      # Create an initial facebook authentication redirect url, a la 
      # https://developers.facebook.com/docs/authentication/server-side/
      facebookurl = 'https://www.facebook.com/dialog/oauth?'
      
      # Add the facebook app ID
      facebookurl += 'client_id='
      facebookurl += settings.FACEBOOK_APP_ID
      
      # Add a redirect url, which must be the same as one indicated in
      # the fb app settings
      facebookurl += '&redirect_uri='
      facebookurl += facebookredirect
      
      # don't think we need additional permissions for now, but if we do,
      # later can uncomment these lines. see 
      # https://developers.facebook.com/docs/authentication/permissions/
      #facebookurl += '&scope='
      #facebookurl += COMMA_SEPARATED_LIST_OF_PERMISSION_NAMES
      
      # To protect against CSRF, add a key which is then checked later
      facebookurl += '&state='
      fb_csrf = "".join([choice(letters+digits) for x in range(1, 40)])
      request.session['fb_csrf'] = fb_csrf
      facebookurl += fb_csrf
      
      return redirect(facebookurl)
   
   else:
      return HttpREsponse('something went wrawng')
