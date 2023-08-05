from setuptools import setup, find_packages
import os

version = '1.0a2'

setup(name='plone.testing',
      version=version,
      description="Testing infrastructure for Zope and Plone packages",
      long_description=open("README.txt").read() + "\n\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read() + "\n\n" +
                       "Detailed documentation\n" +
                       "======================\n\n" +
                       open(os.path.join("src", "plone", "testing", "layer.txt")).read() + "\n\n" +
                       open(os.path.join("src", "plone", "testing", "zca.txt")).read() + "\n\n" +
                       open(os.path.join("src", "plone", "testing", "publisher.txt")).read() + "\n\n" +
                       open(os.path.join("src", "plone", "testing", "zodb.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone zope testing',
      author='Martin Aspeli',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.testing',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.testing',
          'unittest2',
      ],
      extras_require = {
        'test': [
                'zope.component',
                'zope.interface',
                'zope.publisher',
                'zope.security',
                'zope.event',
                'zope.configuration',
                'zope.testbrowser',
                'zope.app.publisher', # XXX: Can probably go away in Zope 2.13
                'ZODB3',
                'Zope2',
            ],
        'zodb': [
                'ZODB3',
            ],
        'zca': [
                'zope.component',
                'zope.event',
                'zope.configuration',
            ],
        'publisher': [
                'zope.configuration',
                'zope.security',
                'zope.app.publisher', # XXX: Can probably go away in Zope 2.13
            ],
        'z2': [
                'Zope2',
                'zope.site',
                'zope.testbrowser',
                'zope.publisher',
            ],
      },
      entry_points="""
      """,
      )
