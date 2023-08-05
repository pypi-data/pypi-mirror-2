from django.shortcuts import render_to_response
from django.template import RequestContext

import utils

def nav_item(request, url):
    """
    Displays a nav item.
    url isn't used, request.path is used instead.
    """
    selected_nav_items = utils.get_selected_nav_items(request)

    if len(selected_nav_items) > 1:
	# page will be a FlatPage by default.
	page = selected_nav_items[-1].content_object
    else:
	page = selected_nav_items[0].content_object

    c = RequestContext(request, {'content_object':page, 'user':request.user})
    return render_to_response('flatpages/default.html', c)
