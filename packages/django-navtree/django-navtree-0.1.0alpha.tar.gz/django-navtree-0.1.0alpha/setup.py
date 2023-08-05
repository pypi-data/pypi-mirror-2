from distutils.core import setup

setup(name='django-navtree',
      version=__import__('navtree').__version__,
      description='Django application for adding hierarchical navigation to projects',
      long_description=open('docs/overview.txt').read(),
      author='Mark Muetzelfeldt',
      author_email='markmuetz@gmail.com',
      url='http://bitbucket.org/markmuetz/django-navtree/',
      packages=['navtree'],
      license='MIT',
      )
