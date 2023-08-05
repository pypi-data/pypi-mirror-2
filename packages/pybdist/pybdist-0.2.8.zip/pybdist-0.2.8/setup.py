#!/usr/bin/env python

from distutils.core import setup
import re

# setup.py sdist --formats=gztar,zip upload
# setup.py bdist

NAME = 'pybdist'
VER = '0.2.8'
DIR = 'src/pybdist'
PY_NAME = 'pybdist'
DEB_NAME = 'python-bdist'
RELEASE_FILE = 'docs/RELEASE.rst'

PY_SRC = '%s.py' % PY_NAME
DEPENDS = ['fakeroot', 'lintian', 'help2man', 'build-essential',
    'python-twitter', 'python-simplejson']
MENU_SUBSECTION = ''
DEPENDS_STR = ' '.join(DEPENDS)
AUTHOR_NAME = 'Scott Kirkwood'
COPYRIGHT_NAME = 'Google Inc.'
GOOGLE_CODE_EMAIL = 'scott@forusers.com'
KEYWORDS = ['python', 'utility', 'library']

SETUP = dict(
  name=NAME,
  version=VER,
  packages=['pybdist'],
  package_dir={
      'pybdist': 'src/pybdist'},
  author=AUTHOR_NAME,
  author_email='scott+pybdist@forusers.com',
  platforms=['POSIX'],
  license='Apache',
  keywords=' '.join(KEYWORDS),
  url='http://code.google.com/p/%s' % NAME,
  download_url='http://%s.googlecode.com/files/%s-%s.zip' % (NAME, NAME, VER),
  description='Python Build Distribution Library (pybdist)',
  long_description="""Library used for personal projects to create a zip, tar and Debian
  distributions.  Assumes folders are in a certain location so might not be
  suitable for other projects. Also supports uploading to code.google.com, pypi,
  """,
  classifiers=[ # see http://pypi.python.org/pypi?:action=list_classifiers
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Apache Software License',
      'Operating System :: POSIX :: Linux',
      'Topic :: Software Development :: Libraries',
  ],
  #zip_safe=False,
)

COPYRIGHT = 'Copyright 2010 %s' % (COPYRIGHT_NAME) # pylint: disable-msg=W0622
LICENSE_TITLE = 'Apache License'
LICENSE_SHORT = 'Apache'
LICENSE_VERSION = '2.0'
LICENSE_TITLE_AND_VERSION = '%s version %s' % (LICENSE_TITLE, LICENSE_VERSION)
LICENSE = '%s or any later version' % LICENSE_TITLE_AND_VERSION # pylint: disable-msg=W0622
LICENSE_TITLE_AND_VERSION_ABBREV = '%s v%s' % (LICENSE_SHORT, LICENSE_VERSION)
LICENSE_ABBREV = '%s+' % LICENSE_TITLE_AND_VERSION_ABBREV
LICENSE_URL = 'http://www.apache.org/licenses/LICENSE-2.0'
LICENSE_PATH = '/usr/share/common-licenses/Apache-2.0'
LICENSE_NOTICE = '''%(name)s is free software: you can redistribute it and/or modify
it under the terms of the Apache License as published by
the Apache Software Foundation, either version 2 of the License, or
(at your option) any later version.

%(name)s is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the Apache License
along with this program.  If not, see <%(url)s>.''' % dict(name=NAME, url=LICENSE_URL)

LICENSE_NOTICE_HTML = '<p>%s</p>' % LICENSE_NOTICE.replace('\n\n', '</p><p>')
LICENSE_NOTICE_HTML = re.sub(r'<http([^>]*)>', r'<a href="http\1" target="_blank">http\1</a>',
    LICENSE_NOTICE_HTML)

if __name__ == '__main__':
  setup(**SETUP)
