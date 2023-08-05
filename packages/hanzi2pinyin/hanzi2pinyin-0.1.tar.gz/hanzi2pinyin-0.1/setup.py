# -*- encoding:utf-8 -*-

from setuptools import setup, find_packages
import sys, os

version = '0.1'
README = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

setup(name='hanzi2pinyin',
      version=version,
      description="汉字转拼音",
      long_description=README,
     classifiers=[
      "Programming Language :: Python",
      'License :: OSI Approved :: BSD License',
          ],
      keywords='chinese hanzi translate pinyin',
      author='Young King',
      author_email='youngking@flyzen.com',
      url='http://www.flyzen.com',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
