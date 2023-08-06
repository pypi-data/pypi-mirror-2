# -*- coding: utf-8 -*-
from codecs import BOM
import glob
import os
from setuptools import setup, find_packages
from django_addons import get_version

with open(u'README') as f:
    long_description = f.read()
if long_description.startswith(BOM):
    long_description = long_description.lstrip(BOM)
long_description = long_description.decode('utf-8')


setup(
    name='django-addons',
    version=get_version().replace(' ', '-'),
    description='Addon framework for Django',
    long_description=long_description,
    author='Dimitris Glezos',
    author_email='glezos@indifex.com',
    url='http://code.indifex.com/django-addons/',
    download_url='http://code.indifex.com/django-addons/get/tip.gz',
    license = 'BSD',
    zip_safe = False,
    packages=find_packages(),
    classifiers=['Development Status :: 4 - Beta',
                'Environment :: Web Environment',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: BSD License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Software Development :: Libraries :: Python Modules',
                'Topic :: Utilities'],
    data_files=[
        ('django_addons/templates', glob.glob('django_addons/templates/*.html')),
    ],
)
