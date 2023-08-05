#!/usr/bin/env python

from distutils.core import setup
import os

NAME='key-train'
VER='0.1.1'

def read(*rnames):
  return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (read('README.txt') +
  '\n'  + 
  'Change History\n' + 
  '==============\n' +
  '\n'  + 
  read('ChangeLog'))

setup(
  name = NAME,
  version = VER,
  packages = ['keytrain'],
  package_dir = {
    'keytrain': 'src/keytrain'},
  package_data = {
    'keytrain': [
        'stats/*',
        'locale/**/**/*',
        'articles/**/**/*',
        '*.yaml',
        '*.svg',
        '*.png',
        'images/*',
        '*.kbd'],
  },
  scripts=['src/key-train'],
  author='Scott Kirkwood',
  author_email='scott@forusers.com',
  platforms=['POSIX'],
  license='Apache Software License',
  keywords='keyboard training education',
  url='http://code.google.com/p/%s' % NAME,
  download_url='http://%s.googlecode.com/files/%s-%s.zip' % (NAME, NAME, VER),
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: X11 Applications',
    'Intended Audience :: Education',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: POSIX :: Linux',
    'Topic :: Education',
  ], 
  description='A typing tutor to help you learn to touch type.',
  long_description=long_description,
)
