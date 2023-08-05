#!/usr/bin/python

import sys
#from distutils.core import setup
from setuptools import setup, find_packages
import sys, os

required = []

if sys.version_info[:3] < (2, 5, 0):
  required.append('elementtree')

setup(
    name='gsmirror',
    version='1.0.2',
    description='Google Sites Mirroring & Backup Script',
    long_description = """\
A Python module and script, which is able to download content from Google Sites (via Sites Data API) and create a mirror of the original web sites, but with a custom design (via Cheetah template) - for hosting on a traditional webserver.

Google Sites then become just an editing interface for the content, which is displayed somewhere else - with the possibility to completely customize the design of the websites.

The complete Sites structure is preserved, including the attachments. The script creates directories and files emulating the original Sites on the local disk. To publish such mirror of the Google Sites, it is enough to copy this directories via FTP to any webserver. We plan to support also direct hosting on the Google App Engine.
""",
    author='Jan Rychtar',
    author_email='honza.rychtar@gmail.com',
    license='New BSD License',
    url='http://code.google.com/p/google-sites-mirror/',
    packages=[ 'gsmirroring' ],
    package_dir = {'gsmirroring':'src/gsmirroring' },
    install_requires= [ 
         'Cheetah',
	 'BeautifulSoup',
         'gdata'
         ],
    package_data = {
        '': ['templates/*'],
        },
    entry_points = """
        [console_scripts]
        gsmirror = gsmirroring.gsmirror:main
    """

)
