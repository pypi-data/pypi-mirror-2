from django import template

register = template.Library()

@register.inclusion_tag('main_nav.html', takes_context=True)
def main_nav(context):
    return context

@register.inclusion_tag('tree_nav.html', takes_context=True)
def tree_nav(context):
    return context

@register.inclusion_tag('breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    return context

#class BreadCrumbsNode(template.Node):
#    def __init__(self, breadcrumbs_list, is_title=''):
#	self.breadcrumbs_list = breadcrumbs_list	
#	self.is_title = is_title	
#
#    def render_title(self, context):
#	# TODO: DRY!
#	breadcrumbs_list = self.breadcrumbs_list.resolve(context, True)
#
#	if len(breadcrumbs_list) == 0:
#	    format_string = "webflow"
#	else:
#	    format_string = "webflow &gt; "
#
#	    for i in range(len(breadcrumbs_list) - 1):
#		title = "%s &gt; " % (breadcrumbs_list[i])
#		format_string = "%s%s" % (format_string, title)
#
#	    format_string = "%s %s" % (format_string, breadcrumbs_list[-1])
#
#	return format_string
#
#    def render(self, context):
#	breadcrumbs_list = self.breadcrumbs_list.resolve(context, True)
#	print 'render breadcrumbs tag'
#	if self.is_title == 'title':
#	    return self.render_title(context)
#
#	if len(breadcrumbs_list) == 0:
#	    format_string = "webflow"
#	else:
#	    format_string = "<a href='/'>webflow</a> &gt; "
#
#	    for i in range(len(breadcrumbs_list) - 1):
#		# TODO: URL is essentiall hard coded in.
#		url = "<a href='/"
#		for k in range(i + 1):
#		    url = "%s%s/" % (url, breadcrumbs_list[k])
#		url = "%s'>%s</a> &gt; " % (url, breadcrumbs_list[i])
#
#		format_string = "%s%s" % (format_string, url)
#
#	    format_string = "%s %s" % (format_string, breadcrumbs_list[-1])
#
#	return format_string
#
#def breadcrumbs(parser, token):
#    bits = token.split_contents()
#    breadcrumbs_list = parser.compile_filter(bits[1])
#    print len(bits)
#    if len(bits) == 3:
#	print bits[2]
#	return BreadCrumbsNode(breadcrumbs_list, bits[2])
#    else:
#	return BreadCrumbsNode(breadcrumbs_list)
#
#register.tag('breadcrumbs', breadcrumbs)
