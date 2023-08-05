import os

from django.conf.urls.defaults import *
from django.contrib import admin

from settings import DEBUG, ROOTDIR

admin.autodiscover()

urlpatterns = patterns('')

if DEBUG:
  urlpatterns += patterns('',
    (r'^site-media/css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(ROOTDIR, 'site-media/css')}),
    (r'^site-media/img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(ROOTDIR, 'site-media/img')}),
    (r'^site-media/js/(?P<path>.*)$',  'django.views.static.serve', {'document_root': os.path.join(ROOTDIR, 'site-media/js')}),
  )

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)), 

    #(r'^admin/(.*)', admin.site.root),
    (r'^', include('navtree.urls')),
)
