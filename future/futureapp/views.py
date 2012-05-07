from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from urllib import quote
from models import *
from os import getenv
import re
from django.conf import settings
import string
from random import choice
import requests
from facepy import GraphAPI
from datetime import datetime, timedelta
import smtplib
from email.utils import formatdate
from django.db.utils import IntegrityError
from django.contrib.contenttypes.models import ContentType
from itertools import chain
# Create your views here.

# Drop page: either render splash or homepage
def drop(request):
   if request.session.get('logged_in'):
      return renderHomepage(request)
   else:
      return render_to_response('splash.html')

# Render homepage with posts from DB:
def renderHomepage(request):
   # check that user is logged in:
   if request.session.get('logged_in'):
       posts = UserPost.objects.order_by('-time')
       hashtags = Tag.objects.all()
       curUser = User.objects.filter(pk = request.session['uid'])
       curUser = curUser[0]    #querydict
       c = RequestContext(request, {'post_list':posts,'tags_list':hashtags,
               'curUser':curUser,})
       return render_to_response('home.html', c)
   else:
       return redirect('/fbauth/')


# Render homepage with posts from DB:
def renderProfile(request, name):
   # check that user is logged in:
   if request.session.get('logged_in'):
      curUser = User.objects.filter(pk = request.session['uid'])
      curUser = curUser[0]    #querydict
       
      name = re.split('-', name)
      name = name[0]
      try:
         profileUser = User.objects.filter(firstname__iexact = name)
         profileUser = profileUser[0]
      except:
         return HttpResponse("User %s does not exist." % name)
      authoredPosts = UserPost.objects.filter(author=profileUser.pk).order_by('-time')
      c = RequestContext(request, {'post_list':authoredPosts,
                                   'curUser':curUser,})
      return render_to_response('profile.html', c)
   else:
      return redirect('/fbauth/')

# Renders the homepage, hashtag filtered.  Works very much the same way as
# renderHomepage.
def renderHashfiltered(request,hashtag):
# -----
   # Note: Hashtagging was implemented while referring to code from
   # https://github.com/semente/django-hashtags
# -----

# check that user is logged in:
   if request.session.get('logged_in'):
       try:
          T = Tag.objects.get(text=hashtag)
       except:
          return HttpResponse("Hashtag %s does not exist." % hashtag)
       posts = UserPost.objects.filter(Tags = T)
       posts = posts.order_by('-time')
       hashtags = Tag.objects.all()
       curUser = User.objects.filter(pk = request.session['uid'])
       curUser = curUser[0]    #querydict
       comments = Comment.objects.all()
       hashTagView = True
       hashtags = Tag.objects.all()
       c = RequestContext(request, {'post_list':posts,
               'curUser':curUser, 'tag_view': hashTagView, 'hash': hashtag, 'tags_list':hashtags,})
       return render_to_response('home.html', c)
   else:
       return redirect('/fbauth/')
   
   
# renders the directory page
def directory(request):
   if request.session.get('logged_in'):
       members = User.objects.all();
       curUser = User.objects.filter(pk = request.session['uid'])
       curUser = curUser[0]    #querydict

       sophomores = members.filter(year='2014')
       notfriends = sophomores.exclude(friends__pk=curUser.pk)
       friends = sophomores.filter(friends__pk=curUser.pk)
       for friend in friends:
          friend.isfriend = True
       sophomores = list(chain(friends, notfriends))
       
       juniors = members.filter(year='2013')
       notfriends = juniors.exclude(friends__pk=curUser.pk)
       friends = juniors.filter(friends__pk=curUser.pk)
       for friend in friends:
          friend.isfriend = True
       juniors = list(chain(friends, notfriends))

       seniors = members.filter(year='2012')
       notfriends = seniors.exclude(friends__pk=curUser.pk)
       friends = seniors.filter(friends__pk=curUser.pk)
       for friend in friends:
          friend.isfriend = True
       seniors = list(chain(friends, notfriends))
       
       
       c = RequestContext(request, {'sophmore_list':sophomores,
                                    'junior_list':juniors,
                                    'senior_list':friends,
                                    'curUser':curUser,
                                    'fbappid':settings.FACEBOOK_APP_ID,
                                    })
       return render_to_response('directory.html', c)
   else:
       return redirect('/fbauth/')

# show all announcements
def renderAnnouncements(request):
   # check that user is logged in:
  if request.session.get('logged_in'):
      posts = UserPost.objects.filter(announce=True)
      posts = posts.order_by('-time')
      hashtags = Tag.objects.all()
      curUser = User.objects.filter(pk = request.session['uid'])
      curUser = curUser[0]    #querydict
      c = RequestContext(request, {'post_list':posts,'tags_list':hashtags,
              'curUser':curUser,})
      return render_to_response('home.html', c)
  else:
      return redirect('/fbauth/')

# render the menu page:
def renderMenu(request):
   if request.session.get('logged_in'):
       # get curUser:
       members = User.objects.all();
       curUser = User.objects.filter(pk = request.session['uid'])
       curUser = curUser[0]    #querydict
       # determine post access:
       a = curUser.admin
       if(a == u'FC' or a == u'BAMF'):
           postPerm = True;
       else:
           postPerm = False;
       # get all menu posts:
       menus = MenuPost.objects.order_by('-time')

       c = RequestContext(request, {'menu_list':menus,
               'curUser':curUser, 'postPerm':postPerm})
       return render_to_response('menu.html', c)
   else:
       return redirect('/fbauth/')

# ----      Menu Manipulation       ----#

# make a new menu
def postMenu(request):
    if request.method == 'POST':
        #get curuser
        curAuthor = User.objects.filter(pk = request.session['uid'])
        curAuthor = curAuthor[0]    #it's a querydict
        # check permissions
        a = curAuthor.admin
        if(a == u'FC' or a == u'BAMF'):
            newMenu = MenuPost(title = 'foo', #title=request.POST['title'],
                               text = request.POST['text'],
                               author = curAuthor,
                 #             tags = (),
                 #             mentions = ()
                                             )
            newMenu.save()
            return renderMenu(request) 
        else:
            return HttpResponse('You do not have permission to post menus.') 
    else:
        # we need to change this to a more general-purpose error.
        # Control flow reaches here if the user tries to go to the posting url
        # without actually making a post.
        return HttpResponse('Menu Posting failed!')


#delete a menu:
def deleteMenu(request):
    if request.method == 'POST':
        #check author
        curUser = User.objects.filter(pk = request.session['uid'])
        curUser = curUser[0]    #querydict
        # check permissions
        a = curUser.admin
        if(a == u'FC' or a == u'BAMF'):
            id = request.POST['postMenu']
            p = MenuPost.objects.get(pk = id)
            p.delete()
            return renderMenu(request)
        else:
            return HttpResponse('You do not have permission to delete menus.') 
    else:
        return HttpResponse('Menu deletion failed!')


# ----      UserPost Manipulation       ----#

# make a new UserPost.
def post(request):
    if request.method == 'POST':
        curAuthor = User.objects.filter(pk = request.session['uid'])
        curAuthor = curAuthor[0]    #it's a querydict
        posttext = request.POST.get('text', '')
        if posttext == '':
           return HttpReseponse('You must enter text.')
        newPost = UserPost(title = 'foo', #title=request.POST['title'],
                     text = posttext,
                     author = curAuthor,
                     hasvideo = False,
        #             tags = (),
        #             mentions = ()
                          )
        # video embedding:
        hasyoutubeurl = re.compile(r"[?&]v=[\w-]{11}")
        vididlist = hasyoutubeurl.findall(posttext)
        if len(vididlist) > 0:
           newPost.youtubeid = vididlist[0][3:]
           newPost.hasvideo = True
        
        # announcements
        is_announcement = request.POST.get('is_announcement','')
        if(is_announcement):
           newPost.announce=True

        newPost.save()
        link_tags_mentions(posttext, newPost)
        return renderHomepage(request) 
    else:
        # we need to change this to a more general-purpose error.
        # Control flow reaches here if the user tries to go to the posting url
        # without actually making a post.
        return HttpResponse('Posting failed!')

# link hashtags to a UserPost:
def link_tags_mentions(text, post):
# ----
   # This code was influenced heavily by code from
   # https://github.com/semente/django-hashtags
# ----
    # search for hashtags:
    hashRe= re.compile(r'[#]+([-_a-zA-Z0-9]+)')
    mentRe= re.compile(r'[@]+([-_a-zA-Z0-9]+)')
    for h in hashRe.findall(text):
       hashtag, created = Tag.objects.get_or_create(text=h)
       if created:
          hashtag.save()
       try:
          post.Tags.add(hashtag)
       except IntegrityError:
          continue
    for m in mentRe.findall(text):
       try:
          u = User.objects.filter(firstname = m)
          if u.count() > 0:
             u = u[0]
             post.mentions.add(u)
       except IntegrityError:
          continue

# make a new Comment.
def postComment(request):
    if request.method == 'POST': 
        curAuthor = User.objects.filter(pk = request.session['uid'])
        curAuthor = curAuthor[0]    #it's a querydict
 #       parentPost = UserPost.objects.filter(fk = request.POST['parentPost'])
#        parentPost = parentPost[0]
        parentPost = request.POST['parentPost']
        parentPost = UserPost.objects.get(id=parentPost)
        newComment = Comment(#title=request.POST['title'],
                     text = request.POST['commenttext'],
                     author = curAuthor,
                     parent = parentPost, 
        #             tags = (),
        #             mentions = ()
                          )
        newComment.save()
        return renderHomepage(request) 
    else:
        # we need to change this to a more general-purpose error.
        # Control flow reaches here if the user tries to go to the posting url
        # without actually making a post.
        return HttpResponse('Commenting failed!')

#delete a UserPost:
def deletePost(request):
    if request.method == 'POST':
        #check author
        curUser = User.objects.filter(pk = request.session['uid'])
        curUser = curUser[0]    #querydict

        id = request.POST['post']
        p = UserPost.objects.filter(pk = id)
        if p.count() == 0:      # if post does not exist... (catch double tap)
            return renderHomepage(request)
        p = p[0]    #p is queryset
        if p.author == curUser or curUser.admin == 'BAMF':
            p.delete()
            return renderHomepage(request)
        else:
            return HttpResponse('You may not delete a post you do not own.')
    else:
        return HttpResponse('Post deletion failed!')

# ----      Authentication       ---- #

# Authenticate user's netid
def signup(request):
    
   # this page should not be accessed by any method other than GET
   if request.method != 'GET':
       return HttpResponse(status=405)
       
   requestnetid = request.GET.get('netid', '')
   if requestnetid == '': # Http GET request has no netid parameter
      return HttpResponse('not a valid signup request')
       
   signup_user = User.objects.filter(netid = requestnetid)
   if signup_user.count() == 0: # netid not found in database
      return HttpResponse('netid not approved for signup')
        
   signup_user = signup_user[0]
   if signup_user.authenticated == True:
      return HttpResponse('netid already authenticated')
   
   # provided code does not match code in database or parameter is empty
   if request.GET.get('authcode', '') != signup_user.authcode:
      return HttpResponse('Please check that signup link is correct, contains incorrect authentication code')


   # make necessary changes in database and session
   signup_user.authenticated = True
   signup_user.save()
   request.session['authuser'] = signup_user;
  
   c = RequestContext(request, {'curUser':signup_user})
   return render_to_response('splash.html')
   #TODO: make a welcome page for the newbies
   #return render_to_response('fbsignup.html', c)

def logout(request):
   request.session.flush()
   return render_to_response('splash.html')

def createuser(request):
   if request.method != 'POST':
      return HttpResponse(status=405)
   if not request.session.get('logged_in', False):
      return redirect('/fbauth/')
   curUser = User.objects.filter(pk = request.session['uid'])[0]
   if curUser.admin != 'BAMF': #TODO: may need to make this officers eventually
      return HttpResponse('Only administrators may create new users')
   
   if request.POST.get('admin', '') == 'BAMF':
      return HttpResponse('Get real, son')

   new_netid = request.POST.get('netid', '')
   new_firstname = request.POST.get('firstname', '')
   new_lastname = request.POST.get('lastname', '')
   new_year = request.POST.get('year', '')
   new_authcode = "".join([choice(string.letters+string.digits) for x in range(1, 40)])
   new_admin = request.POST.get('admin', '')
   
#   try:
   User.objects.create(
      netid = new_netid,
      firstname = new_firstname,
      lastname = new_lastname,
      year = new_year,
      authenticated = False,
      authcode = new_authcode,
      admin = new_admin
      )
 #  except:
 #    return HttpResponse('User could not be created')
   link = settings.BASE_URI
   link += 'signup?netid=' + new_netid
   link += '&authcode=' + new_authcode
   target_email = new_netid + '@princeton.edu'
   subject = 'Web F. Site Registration'
   message = 'Dear ' + new_firstname + ''',

You have been selected to help create the future of our dear mother on the webbernets.

Your mission, should you choose to accept it, is to visit the link below

'''
   message += link
   mime = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            settings.EMAIL_HOST_USER,
                            target_email,
                            subject,
                            formatdate(), message)
   gmail = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
   gmail.ehlo()
   gmail.starttls()
   gmail.ehlo()
   gmail.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
   gmail.sendmail(settings.EMAIL_HOST_USER, target_email, mime)
   gmail.close()
   return newuser(request)

def newuser(request):
   if not request.session.get('logged_in', False):
       return redirect('/fbauth/')
   curUser = User.objects.filter(pk = request.session['uid'])[0]
   if curUser.admin != 'BAMF': #TODO: may need to make this officers eventually
      return HttpResponse('Only administrators may create new users')
   c = RequestContext(request, {'curUser':curUser,})
   return render_to_response('newuser.html', c)


# does facebook authentication.
def fbauth(request):
   # The url for this page, to be passed as a param to facebook for redirection
   facebookredirect =  settings.BASE_URI+ 'fbauth/'
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
               this_user = User.objects.filter(fbid = visitor_fbid)
               if this_user.count() == 0: # if fbid not in db
                  # if user just signed up
                  new_user = request.session.get('authuser', '')
                  if new_user != '':
                     new_user.fbid = visitor_fbid
                     new_user.pic = 'https://graph.facebook.com/' + str(visitor_fbid) + '/picture?type=square'
                     new_user.largepic = 'https://graph.facebook.com/' + str(visitor_fbid) + '/picture?type=large'
                     new_user.save()
                     this_user = new_user
                  else:
                     return HttpResponse('You are not authorized to use this site')
               # TODO: make a welcome page and rejection page  
               else:
                  this_user = this_user[0]
               request.session['logged_in'] = True
               request.session['uid'] = this_user.pk
               

               # update the user's list of friends
               this_user.friends.add(this_user)
               friendsets = graph.get('me/friends?fields=installed', page=True)
               for friendset in friendsets:
                  
                  # friendset includes both data (returned data) and
                  # paging (iterator urls)
                  friendset = friendset['data']
                  
                  # for each friend returned
                  for friend in friendset:

                     # if they have approved the webfsite app
                     if friend.get('installed', False):
                        friend_user = User.objects.filter(fbid = friend['id'])
                        
                        # and can be found in the database
                        if friend_user.count() == 1:
                           friend_user = friend_user[0]
                           
                           # add them as a friend (doesn't matter if
                           # done twice)
                           this_user.friends.add(friend_user)
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
