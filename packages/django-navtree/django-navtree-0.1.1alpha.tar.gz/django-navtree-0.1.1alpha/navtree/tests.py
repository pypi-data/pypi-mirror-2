"""
Tests for the django navtree app.
"""
import unittest

from models import NavItem

class NavTest(unittest.TestCase):
    top_nav_items = []
    nav_items     = []
    sub_nav_items = []

    def setUp(self):
	"""
	Set up creates 5 top level nav items, 3 middle level, and 2 bottom level.
	"""
	for i in range(5):
	    self.top_nav_items.append(NavItem.objects.create(title='Top Test %d' % i, slug='top_test%d' % i, order=i))
	    for j in range(3):
		self.nav_items.append(NavItem.objects.create(parent=self.top_nav_items[i], title='Test %d,%d' % (i, j), slug='test%d-%d' % (i, j), order=j))
		for k in range(2):
		    self.sub_nav_items.append(NavItem.objects.create(parent=self.nav_items[3*i + j], title='Sub Test %d,%d,%d' % (i, j, k), slug='sub_test%d-%d-%d' % (i, j, k), order=k))


    def test_setup(self):
	self.assertEquals(NavItem.objects.all().count(), 50)
	self.assertEquals(NavItem.objects.filter(parent=None).count(), 5)

	top_test2 = NavItem.objects.get(slug='top_test2')
	self.assertEquals(top_test2.order, 2)
	self.assertEquals(top_test2.children.all().count(), 3)
	self.assertEquals(top_test2.children.get(slug='test2-1').children.all()[0].title, 'Sub Test 2,1,0')
