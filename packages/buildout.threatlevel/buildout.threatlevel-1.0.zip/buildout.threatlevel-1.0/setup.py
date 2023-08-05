# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = "1.0"

long_description = open('README.txt').read() + '\n' + open('CHANGES.txt').read()
    
entry_point = 'buildout.threatlevel:install'
entry_points = {"zc.buildout.extension": ["default = %s" % entry_point]}

setup(name='buildout.threatlevel',
      version=version,
      description="A zc.buildout extension that reports the current global buildout threat level",
      long_description=long_description,
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      license='GPL',
      keywords='buildout extension threat',
      author='David Glick',
      author_email='dglick@gmail.com',
      url='http://svn.plone.org/svn/collective/buildout/buildout.threatlevel',
      packages = find_packages(),
      namespace_packages=['buildout'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'
                        ],
      entry_points=entry_points,
      )
