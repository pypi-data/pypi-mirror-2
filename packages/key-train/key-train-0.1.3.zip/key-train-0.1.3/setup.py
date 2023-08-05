#!/usr/bin/env python

# from setuptools import setup, find_packages
from distutils.core import setup
import os
import re

NAME='key-train'
VER='0.1.3'
DIR='src/keytrain'
PY_NAME='key_train'
DEB_NAME=NAME.replace('-', '')

PY_SRC='%s.py' % PY_NAME
DEPENDS=['python-yaml']
MENU_SUBSECTION='Education'
DEPENDS_STR=' '.join(DEPENDS)
AUTHOR_NAME='Scott Kirkwood'
KEYWORDS=['keyboard', 'training', 'education']

def read(*rnames):
  return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

SETUP = dict(
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
        '*.txt',
        '*.yaml',
        '*.svg',
        '*.png',
        'images/*',
        '*.kbd'],
  },
  scripts=['src/key-train'],
  author=AUTHOR_NAME,
  author_email='scott+keytrain@forusers.com',
  platforms=['POSIX'],
  license='Apache 2.0',
  keywords=' '.join(KEYWORDS),
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
  long_description="""Keyboard Training Software (for linux)
A keyboard training program which I'm designing for my 8 year old son.
This is a keyboard training program (i.e. typing tutor) for touch typing, still in it's early days.
Goals:
Open source and open community.
Various languages supported (although not right to left nor logographic writing systems = ex. Kanji) (todo)
Various international keyboards supported and probably dvorak keyboards as well. (todo)
Attractive interface. (todo)
Scalable graphics, make the window as small or as large as you like.
Show the beginner typist where they should place their fingers. (todo)
Interesting text for advanced users instead of just random gibberish. Will pull in text from Wikipedia entries, for
various languages. (todo)
Beginner levels will have random text, however, and they should focus on common bi=grams and trigrams of the language in
question, to build up muscle memory for common key combinations. (todo)
Random text should also start with very simple letter combinations, like two keys close together for training the first
time. (todo)
Stats and progression. (todo)
Heatmap of trouble keys for the student. (todo)
Auto build lessons to work on the trouble keys. (todo)
Lessons for the number keys and punctuation marks. (todo)
Start off without the space bar or the backspace key, add these keys later.
  """,
  #zip_safe=False,
  #install_requires=[
  #  "PyYAML >= 3.0"
  #],
)

COPYRIGHT = 'Copyright (C) 2010 %s' % (AUTHOR_NAME) # pylint: disable-msg=W0622
LICENSE_TITLE = 'Apache License'
LICENSE_SHORT = 'Apache'
LICENSE_VERSION = '2.0'
LICENSE_TITLE_AND_VERSION = '%s version %s' % (LICENSE_TITLE, LICENSE_VERSION)
LICENSE = '%s or any later version' % LICENSE_TITLE_AND_VERSION # pylint: disable-msg=W0622
LICENSE_TITLE_AND_VERSION_ABBREV = 'Apachev%s' % LICENSE_VERSION
LICENSE_ABBREV = '%s+' % LICENSE_TITLE_AND_VERSION_ABBREV
LICENSE_NOTICE = '''%(name)s is free software: you can redistribute it and/or modify
under the compliance of the License.

%(name)s is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.''' % dict(name=NAME)

LICENSE_NOTICE_HTML = '<p>%s</p>' % LICENSE_NOTICE.replace('\n\n', '</p><p>')
LICENSE_NOTICE_HTML = re.sub(r'<http([^>]*)>', r'<a href="http\1" target="_blank">http\1</a>', LICENSE_NOTICE_HTML)

if __name__ == '__main__':
  setup(**SETUP)
