from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='anz.ijabbar',
      version=version,
      description="Integrate iJab(an open source XMPP web chat client recommended by xmpp.org) to your plone site.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone xmpp web chat',
      author='jiangdongjin',
      author_email='eastxing@gmail.com',
      url='http://plone.org/products/anz.ijabbar/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['anz'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'python-cjson',
          'plone.memoize'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],
      )
