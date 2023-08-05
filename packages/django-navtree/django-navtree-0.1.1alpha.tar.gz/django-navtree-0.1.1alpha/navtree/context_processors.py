from models import NavItem
import utils

def nav_tree(request):
    try:
	selected_nav_items = utils.get_selected_nav_items(request)
	if len(selected_nav_items) != 1:
	    selected_top_nav_item, child = selected_nav_items[0], selected_nav_items[-1]
	else:
	    selected_top_nav_item, child = selected_nav_items[0], None
    except:
	return {}

    # Generate the nav data.
    top_nav_items = []
    for top_nav_item in NavItem.objects.filter(parent=None).order_by('order'):
	nav_col = []
	for nav_item in top_nav_item.children.all().order_by('order'):
	    sub_nav_col = []
	    for sub_nav_item in nav_item.children.all().order_by('order'):
		if sub_nav_item in selected_nav_items:
		    selected = True
		else:
		    selected = False
		sub_nav_col.append({'id': sub_nav_item.id, 
				    'title': sub_nav_item.title, 
				    'url': sub_nav_item.url(), 
				    'selected': selected, 
				    'colour': sub_nav_item.colour  })

	    if nav_item in selected_nav_items:
		selected = True
	    else:
		selected = False
	    nav_col.append({'id': nav_item.id, 
			    'title': nav_item.title, 
			    'url': nav_item.url(), 
			    'selected': selected, 
			    'col': sub_nav_col, 
			    'colour': nav_item.colour  })
	if top_nav_item == selected_top_nav_item:
	    selected = True
	else:
	    selected = False
	top_nav_items.append({'id': top_nav_item.id, 
			      'title': top_nav_item.title, 
			      'url': top_nav_item.url(), 
			      'selected': selected, 
			      'col': nav_col, 
			      'colour':top_nav_item.colour  })

    return {'selected_nav_items': selected_nav_items, 'top_nav_items': top_nav_items}
