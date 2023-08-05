from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.portlet.rssjs',
      version=version,
      description="Rss Portlet using javascript to get, parse and render an RSS feed on the client",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Hans-Peter Locher',
      author_email='hans-peter.locher@inquant.de',
      url='http://svn.plone.org/svn/collective/collective.portlet.rssjs/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
