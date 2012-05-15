from django.conf.urls.defaults import patterns, include, url
from django.http import HttpResponse
from futureapp.views import * 
from django.conf import settings

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
                       )

urlpatterns += patterns('',
                        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                        )
