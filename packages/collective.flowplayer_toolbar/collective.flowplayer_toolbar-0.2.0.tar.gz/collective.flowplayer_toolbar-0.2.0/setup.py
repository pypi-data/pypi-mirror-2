from setuptools import setup, find_packages
import os

version = '0.2.0'

setup(name='collective.flowplayer_toolbar',
      version=version,
      description="A Plone module which add an accessible Javascript controlsbar to collective.flowplayer",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Video",
        ],
      keywords='plone flowplayer javascript player toolbar accessibility',
      author='RedTurtle Technology',
      author_email='luca.fabbri@redturtle.net',
      url='http://svn.plone.org/svn/collective/collective.flowplayer_toolbar/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.flowplayer>3.0dev',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],
      )
