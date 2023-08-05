from django.contrib.sitemaps import Sitemap 
from models import NavItem

class NavigationSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
	return NavItem.objects.all()

    def location(self, item):
	return item.url()
