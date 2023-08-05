from setuptools import setup, find_packages
import os

version = '0.1.1a'

setup(name='collective.colorbox',
      version=version,
      description="A jQuery plugin that provides lightboxes in Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Programming Language :: JavaScript",
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: User Interfaces",
        ],
      keywords='plone slideshow lightbox jquery colorbox',
      author='David Bain',
      author_email='pigeonflight@gmail.com',
      url='http://plone.org/products/collective.colorbox',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
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
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
