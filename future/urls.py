from django.conf.urls.defaults import patterns, include, url
from django.http import HttpResponse
from futureapp.views import * 
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# ----
  # this function influenced by:
  # https://github.com/semente/django-hashtags
#-----
hashtagged_url = url(
                regex  = '^(?P<hashtag>[-\w]+)/$',
                view = renderHashfiltered,
                name = 'hashtagged_url'
                )

urlpatterns = patterns('',
                       url(r'^$',drop),
                       url(r'^post/$',post),
                       url(r'^deletePost/$',deletePost),
                       url(r'^home/$',renderHomepage),
                       url(r'^fbauth/$',fbauth),
                       url(r'^signup/$',signup),
                       url(r'^newuser/$',newuser),
                       url(r'^createuser/$',createuser),
                       url(r'^directory/$',directory),
                       url(r'^menu/$',renderMenu),
                       url(r'^postMenu/$',postMenu),
                       url(r'^announcements/$',renderAnnouncements),
                       url(r'^deleteMenu/$',deleteMenu),
                       url(r'^logout/$',logout),
                       url(r'^postComment/$',postComment),
                       url(r'^deleteComment/$',deleteComment),
                       url(r'^user/(\w+-\w+)/$', renderProfile),
                       url(r'^search/$', search),
                       hashtagged_url,

                       #url(r'^home/$', 'django.views.generic.simple.direct_to_template', {'template': 'future/static2.html'})
                       # Examples:
                           # url(r'^$', 'future.views.home', name='home'),
                       # url(r'^future/', include('future.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                           # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                           # url(r'^admin/', include(admin.site.urls)),
                       )
urlpatterns += patterns('',
                        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                        )
