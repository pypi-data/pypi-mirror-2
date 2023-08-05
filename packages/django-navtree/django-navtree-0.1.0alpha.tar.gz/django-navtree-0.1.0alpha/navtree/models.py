from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.conf import settings

USE_FLATPAGES     = getattr(settings, 'NAVIGATION_USE_FLATPAGES', True)

class NavItem(models.Model):
    parent = models.ForeignKey('NavItem', blank=True, null=True, related_name='children')
    if USE_FLATPAGES:
	# This is the default state.
	content_object   = models.OneToOneField(FlatPage, blank=True, null=True, related_name='nav_item')
    else:
	# This can be used to create links to any other django model.
	# to use put NAVIGATION_USE_FLATPAGES = True in your settings file. 
	# Will work out of the box if the model being linked to has a 'content'
	# method/field.
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')


    title  = models.CharField(max_length=100)
    slug   = models.CharField(max_length=100)

    order  = models.IntegerField()
    colour = models.CharField(max_length=7, default='#0000FF')
    image  = models.ImageField(upload_to='img', blank=True, null=True)

    def get_absolute_url(self):
	return self.url()

    def url(self, from_child=False):
	# if from_child is True, then this is being called recursively from child:
	# just return self.slug. Else, try to return the url of first child (if exists).
	if self.parent:
	    # Call recursively
	    return "%s%s/" % (self.parent.url(from_child=True), self.slug)
	elif from_child:
	    return "/%s/" % (self.slug)
	else:
	    try:
		return "/%s/%s/" % (self.slug, self.children.get(order=0).slug)
	    except:
		return "/%s/" % (self.slug)

    def __unicode__(self):
	return self.title
