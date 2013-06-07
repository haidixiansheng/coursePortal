from django.conf.urls import patterns, include, url
from web import urls as web_urls
from assignment import urls as assignment_urls
#from djangobb_forum import urls as djangobb_forum_urls
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include(web_urls)),
    url(r'^assignment/', include(assignment_urls)),
    #url(r'^forum/', include(djangobb_forum_urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'forum/', include('pybb.urls', namespace = 'pybb')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)