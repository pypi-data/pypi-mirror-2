from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^(?P<url>.*)$', views.nav_item, {}, 'nav_item'),
)
