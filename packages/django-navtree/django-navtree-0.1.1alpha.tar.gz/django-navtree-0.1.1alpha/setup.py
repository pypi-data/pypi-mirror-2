from distutils.core import setup

setup(name='django-navtree',
      version=__import__('navtree').__version__,
      description='Django application for adding hierarchical navigation to projects',
      long_description=open('docs/overview.txt').read(),
      author='Mark Muetzelfeldt',
      author_email='markmuetz@gmail.com',
      url='http://bitbucket.org/markmuetz/django-navtree/',
      requires=["django (>=1.2)", "PIL"],
      packages=['navtree'],
      license='MIT',
      classifiers=[
        'Programming Language :: Python',
        'Framework :: Django',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
      ],
)
