from models import NavItem

def get_selected_nav_items(request):
    """ 
    This function creates request.selected_nav_items, a list containing each nav
    item (0th is top level). It does this by looking at the requested URL
    and adding getting each nav item. If it has been called before with the same
    request object, it just returns request.selected_nav_items, which has already
    been filled in.
    """

    try:
	return request.selected_nav_items
    except:
	pass

    url = request.path

    request.selected_nav_items = []

    # Decode the url, which is canonically named, separated by '/'s
    parent, child = None, None
    for slug in url.split('/'):
	if slug == '':
	    continue
	if parent == None:
	    parent = NavItem.objects.get(slug=slug, parent=parent)
	else:
	    child = NavItem.objects.get(slug=slug, parent=parent)
	    parent = child

	request.selected_nav_items.append(parent)

    if len(request.selected_nav_items) == 0:
	# If no page is given in URL, show home page (assumed to be first top level nav item)
	request.selected_nav_items.append(NavItem.objects.get(order=0, parent=None))
    
    return request.selected_nav_items
