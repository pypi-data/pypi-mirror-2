from setuptools import setup, find_packages
import os

version = '1.1.1'

setup(name='plone.app.openid',
      version=version,
      description="Plone OpenID authentication support",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Plone OpenID authentication consumer',
      author='Wichert Akkerman, Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/plone.app.openid',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages = ['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'plone.openid',
        'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
