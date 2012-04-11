from django.conf.urls.defaults import patterns, include, url
from futureapp.views import post 

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^post/$',views.post),
    # Examples:
    # url(r'^$', 'future.views.home', name='home'),
    # url(r'^future/', include('future.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
