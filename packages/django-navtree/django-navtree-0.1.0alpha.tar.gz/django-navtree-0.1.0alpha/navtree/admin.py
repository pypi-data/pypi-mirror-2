from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.contenttypes import generic
from django.conf import settings

from models import *

USE_FLATPAGES     = getattr(settings, 'NAVIGATION_USE_FLATPAGES', True)

if USE_FLATPAGES:
    class NavItemInline(admin.TabularInline):
	model = NavItem

    class FlatPageAdmin(admin.ModelAdmin):
	# TODO: how to get this to appear at top of admin page?
	inlines = [ NavItemInline, ]
	# Taken from flatpage admin and modified.
	fieldsets = (
		(None, {
		    'fields': ('title', 'content', 'url', 'sites')
		    }),
		('Advanced options', {
		    'classes': ('collapse',),
		    'fields': ('enable_comments', 'registration_required', 'template_name')
		    }),
		)

    admin.site.unregister(FlatPage)
    admin.site.register(FlatPage, FlatPageAdmin)

else:
    class NavItemAdmin(admin.ModelAdmin):
	pass

    class NavItemInline(generic.GenericTabularInline):
	"""
	This class can be added as an inline to any other class' admin class, allowing
	you to edit the NavItem class from the other class' admin page.
	"""
	model = NavItem

class NavItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
	    (None, {
		'fields': ('parent', 'content_object', 'title', 'slug', 'order')
		}),
	    ('Extra options', {
		'fields': ('colour', 'image') }),
	    )
    list_display = ('title', 'parent', 'order', 'colour')
    list_filter = ('parent',)

admin.site.register(NavItem, NavItemAdmin)
