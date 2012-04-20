from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from urllib import quote
from models import *
from os import getenv
from django.conf import settings
import string
from random import choice
import requests
from facepy import GraphAPI
from datetime import datetime, timedelta
# Create your views here.

# Render homepage with posts from DB:
def renderHomepage(request):
   # check that user is logged in:
   if request.session.get('logged_in'):
       posts = UserPost.objects.all();
       c = RequestContext(request, {'post_list':posts,
                                'uid':request.session['uid']})
       return render_to_response('home.html', c)
   else:
       return redirect('/fbauth/')

# Authenticate user's netid
def netidauth(request):
    if request.method == 'POST':
        if netidapproved(request.POST.get('netid')):
            pass # send email
        else:
            pass  # render response: sorry, not a valid netid
    #return redirect('/home/')
    return render_to_response('enternetid.html', c)

def directory(request):
   if request.session.get('logged_in'):
       members = User.objects.all();
       c = RequestContext(request, {'member_list':members,
                                'uid':request.session['uid']})
       return render_to_response('directory.html', c)
   else:
       return redirect('/fbauth/')
   

def netidapproved(netid):
   return True

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
        return renderHomepage(request) 
    else:
        # we need to change this to a more general-purpose error.
        # Control flow reaches here if the user tries to go to the posting url
        # without actually making a post.
        return HttpResponse('Posting failed!')

#delete a post:
def deletePost(request):
    if request.method == 'POST':
        #delete the post from the database
        id = request.POST['post']
#        id = p.get(pk)
        dbp = UserPost.objects.get(pk = id)
        dbp.delete()
        return renderHomepage(request)
    else:
        return HttpResponse('Post deletion failed!')

def fbauth(request):
   # The url for this page, to be passed as a param to facebook for redirection
   facebookredirect = settings.BASE_URI + 'fbauth/'
   facebookredirect = quote(facebookredirect, '')
   
   # if the incoming request is a redirect from facebook with a code
   # that may be exchanged for an oauth token
   if request.method == 'GET':
      
      # if already has an active facebook session
      if request.session.get('fb_token', '') != '':
         
         # if the token is not expired, else fall through to acquire a
         # new one
         if request.session.get('fb_expiry', datetime.now()) > datetime.now():
            
            # if logged in (probably reached this page by accident)
            if request.session.get('logged_in', False):
               return renderHomepage(request)

            # if not logged in, look through the database for the fbid in
            # the session
            else:
               graph = GraphAPI(request.session['fb_token'])
               visitor_fbid = int(graph.get('me')['id'])
               #return HttpResponse(str(visitor_fbid))
               user = User.objects.filter(fbid = visitor_fbid)
               if user.count() == 0: # if fbid not in db
                  request.session['approved_fb'] = True
                  return redirect('/netidauth/')
               else: # if fbid in db already
                  request.session['logged_in'] = True
                  request.session['uid'] = user[0].pk
                  return renderHomepage(request)
      
      # if this is a response from facebook with a code to grab a csrf token
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
            
            # Body is of format token and expiry time, split into
            # appropriate parts
            tokenized = gettoken.text.split('&')
            token = tokenized[0].split('=')[1]
            expiry = int(tokenized[1].split('=')[1])
            request.session['fb_token'] = token
            request.session['fb_expiry'] = datetime.now() + timedelta(seconds = expiry)
            #return HttpResponse('sup')
            return redirect('/fbauth/')

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
      fb_csrf = "".join([choice(string.letters+string.digits) for x in range(1, 40)])
      request.session['fb_csrf'] = fb_csrf
      facebookurl += fb_csrf
      
      return redirect(facebookurl)

   # this page should not be accessed through any method but GET
   else:
      return HttpResponse(status=405)
