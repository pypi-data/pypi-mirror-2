#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

You'll need:
sudo apt-get install help2man fakeroot python-twitter python-simplejson

You'll also need ~/.netrc ~/.ssh/<fname>
"""

__author__ = 'Scott Kirkwood (scott+pybdist@forusers.com)'
__version__ = '0.2.0'

import codecs
import distutils.core
import getpass
import glob
import googlecode_upload
import httplib
import netrc
import os
import re
import release
import shutil
import simplejson
import subprocess
import twitter
import sys

import debian
import googlecode_update


def _GetPySourceVersion(setup):
  fname = '%s/%s' % (setup.DIR, setup.PY_SRC)
  re_py_ver = re.compile(r'__version__\s*=\s*[\'"](.*)[\'"]')
  grps = re_py_ver.search(open(fname).read())
  if not grps:
    print 'Unable to find __version__ in %r' % fname
    sys.exit(-1)
  source_ver = grps.group(1)
  return source_ver


def GetAndVerifyVersions(setup):
  """Get the version and make sure all versions are synched."""
  setup_ver = setup.VER
  source_ver = _GetPySourceVersion(setup)

  release_regex = _GetVar(setup, 'RELEASE_FORMAT')
  rel_ver, rel_date, rel_lines = _ParseLastRelease(setup)
 
  changelog_ver, cl_date, cl_lines = release.ParseDebChangelog(
      'debian/changelog')

  gc_ver, gc_date, gc_lines = release.GetLastGoogleCodeVersion(setup.NAME)
  if gc_ver and gc_ver == setup_ver:
    print 'The code.google.com version is up-to-date'
  if (setup_ver != source_ver or setup_ver != rel_ver 
      or setup_ver != changelog_ver):
    print 'Setup versions don\'t agree'
    print 'setup.py = %r' % setup_ver
    print '%s/%s = %r' % (setup.DIR, setup.PY_SRC, source_ver)
    print '%s = %r' % (setup.RELEASE_FILE, rel_ver)
    print '%s = %r' % ('debian/changelog', changelog_ver)
    print 'code.google.com = %r' % gc_ver
    sys.exit(-1)
  print 'Setup versions agree'
  return setup_ver


def _ParseLastRelease(setup):
  """Parse the release file from setup information.
  Returns:
    rel_ver, relase_date, rel_lines
  """
  release_regex = _GetVar(setup, 'RELEASE_FORMAT')
  return release.ParseLastRelease(
      setup.RELEASE_FILE, release_regex)


def ParseLastRelease(setup):
  _, rel_date, rel_lines = _ParseLastRelease(setup)
  return rel_date, rel_lines


def BuildZipTar(unused_setup):
  ret = subprocess.call([
    'python', 'setup.py', 'sdist', '--formats=gztar,zip'])
  if ret:
    print 'Error building sdist'
    sys.exit(-1)
  print 'Built zip and tar'


def UploadToPyPi(unused_setup):
  ret = subprocess.call([
    'python', 'setup.py', 'sdist', '--formats=zip', 'upload',])
  if ret:
    print 'Error uploading to pypi'
    print 'If it\'s the first time, run "python setup.py register"'
    sys.exit(-1)
  print 'Upload to pypi'


def BuildMan(setup):
  if not hasattr(setup, 'MAN_FILE') or not setup.MAN_FILE:
    return
  try:
    dest_dir = os.path.dirname(setup.MAN_FILE)
    if not os.path.isdir(dest_dir):
      print 'Making directory %r' % dest_dir
      os.makedirs(dest_dir)
    include_file = setup.MAN_FILE.replace('.1', '.include')
    ret = subprocess.call([
      'help2man',
      '%s/%s' % (setup.DIR, setup.PY_SRC),
      #'%s' % setup.NAME,
      '-N', # no pointer to TextInfo
      '-i', include_file,
      '-o', setup.MAN_FILE])
    if ret:
      print 'Failed to build man file'
      sys.exit(-1)

    print 'Built %s.1' % setup.NAME
  except Exception, e:
    print 'You may need to install help2man', e
    sys.exit(-1)


def _GetVar(setup, var):
  if hasattr(setup, var):
    return getattr(setup, var)
  return None


def BuildDeb(setup):
  debian.BuildDeb(setup)


def GetDebFilenames(setup):
  debs = 'dist/%s_%s*all.deb' % (setup.DEB_NAME, setup.VER)
  ret = []
  for deb in glob.glob(debs):
    ret.append(deb)
  return ret


def CleanConfig(setup):
  config_file = os.path.expanduser('~/.config/%s/config' % setup.NAME)
  if os.path.exists(config_file):
    os.unlink(config_file)


def _CleanDoc(setup):
  if not setup.NAME:
    sys.exit(-2)
  docs = '/usr/share/doc/%s' % setup.NAME
  if os.path.exists(docs) and os.path.isdir(docs):
    print 'rm -r %s' % docs
    shutil.rmtree(docs)


def _CleanMan(setup):
  if not setup.NAME:
    sys.exit(-2)
  man = '/usr/share/man/man1/%s.1.gz' % setup.NAME
  if os.path.exists(man):
    print 'rm %s' % man


def _CleanScripts(setup):
  if 'scripts' not in setup.SETUP:
    return
  for script in setup.SETUP['scripts']:
    if not script.strip():
      sys.exit(-3)
    bin_script = '/usr/local/bin/%s' % os.path.basename(script)
    if os.path.exists(bin_script):
      print 'rm %s' % bin_script
      os.unlink(bin_script)


def _CleanPackages(setup):
  dist_dirs = ['/usr/share/pyshared',
      '/usr/local/lib/python2.4/dist-packages',
      '/usr/local/lib/python2.5/dist-packages',
      '/usr/local/lib/python2.6/dist-packages']
  base_dir = os.path.basename(setup.DIR)
  if not base_dir.strip():
    print '%r is not a good name' % setup.DIR
    sys.exit(-1)
  for dist_dir in dist_dirs:
    if not os.path.exists(dist_dir):
      continue
    dist_packages = '%s/%s' % (dist_dir, base_dir)
    if os.path.exists(dist_packages):
      print 'rm -r %s' % dist_packages
      shutil.rmtree(dist_packages)
    _CleanEggs(dist_dir, setup)


def _CleanEggs(dist_dir, setup):
  dist_egg = '%s/%s-*.egg-info' % (dist_dir, setup.PY_NAME)
  for fname in glob.glob(dist_egg):
    if os.path.exists(fname):
      if os.path.isdir(fname):
        print 'rm -r %s' % fname
        shutil.rmtree(fname)
      else:
        print 'rm %s' % fname
        os.unlink(fname)


def CleanAll(setup):
  CleanConfig(setup)
  _CleanPackages(setup)
  _CleanDoc(setup)
  _CleanMan(setup)
  _CleanScripts(setup)


def _UploadToGoogleCode(project, fname, username, password):
  print 'Uploading %s' % fname
  dirname = 'dist'
  summary = fname
  if fname.endswith('.zip') or fname.endswith('.tar.gz'):
    labels = ['Type-Source', 'OpSys-Linux', 'Featured']
  elif fname.endswith('.deb'):
    labels = ['Type-Package', 'OpSys-Linux', 'Featured']
  else:
    labels = None
  googlecode_upload.upload(
      '%s/%s' % (dirname, fname),
      project, username, password, summary, labels)
  print 'Done.'


def GetPassFrom(fname):
  """Retrieves the password from this file.
  Verifies that the password is not visible by others on the machine.
  Args:
    fname: ex. ~/.ssh/myuser
  Returns:
    None or the password.  May output stuff too.
  """
  fname = os.path.expanduser(fname)
  if os.path.exists(fname):
    mode = os.stat(fname).st_mode
    if mode & 0077:
      print 'Change permissions on file first, chmod 600 %r' % fname
      return None
    dirname = os.path.dirname(fname)
    mod = os.stat(dirname).st_mode
    if mode & 0077:
      print 'Change permission on directory first, chmod 700 %r' % dirname
      return None
    return file(fname).read().rstrip()
  else:
    print '%r not found' % fname
  return None


def UploadToGoogleCode(setup):
  print 'Using user %r' % setup.GOOGLE_CODE_EMAIL
  password = GetPassFrom('~/.ssh/%s' % setup.GOOGLE_CODE_EMAIL)
  if not password:
    # Read password if not loaded from svn config, or on subsequent tries.
    print 'Please enter your googlecode.com password.'
    print '** Note that this is NOT your Gmail account password! **'
    print 'It is the password you use to access repositories,'
    print 'and can be found here: http://code.google.com/hosting/settings'
    password = getpass.getpass()
  username = setup.GOOGLE_CODE_EMAIL
  _UploadToGoogleCode(setup.NAME, '%s-%s.zip' % (setup.NAME, setup.VER),
      username, password)
  _UploadToGoogleCode(setup.NAME, '%s-%s.tar.gz' % (setup.NAME, setup.VER),
      username, password)
  for deb in GetDebFilenames(setup):
    _UploadToGoogleCode(setup.NAME, deb.replace('dist/', ''), username, password)


def AnnounceOnFreshmeat(setup):
  """Announce launch on freshmeat."""
  print 'Announcing on Freshmeat...'

  rel_ver, rel_date, rel_lines = _ParseLastRelease(setup)
  rc = netrc.netrc(os.path.expanduser('~/.netrc'))
  # Storing the auth_code as the account in the .netrc file
  # ex. chmod 600 ~/.netrc
  # machine freshmeat
  #     login myname
  #     account auth_code_given_by_freshmeat
  #     password mypassword
  auth_code = rc.authenticators('freshmeat')[1]
  name = setup.NAME
  tag = 'Bug fixes'
  if setup.VER.endswith('.0'):
    tag = 'Feature enhancements'
  changelog = ['Changes: '] + rel_lines
  release_dict = dict(version=setup.VER, changelog='\n'.join(changelog), tag_list=tag)
  path = '/projects/%s/releases.json' % name
  body = codecs.encode(simplejson.dumps(dict(auth_code=auth_code, release=release_dict)))
  connection = httplib.HTTPConnection('freshmeat.net')
  connection.request('POST', path, body, {'Content-Type': 'application/json'})
  response = connection.getresponse()
  if response.status != 201:
    print 'Request failed: %d %s' % (response.status, response.reason)
  print 'Done announcing on Freshmeat.'


def AnnounceOnTwitter(setup):
  print 'Announcing on twitter...'
  rc = netrc.netrc(os.path.expanduser('~/.netrc'))
  auth = rc.authenticators('twitter')
  username = auth[0]
  password = auth[2]
  metadata = dict(version=setup.VER, name=setup.NAME, url=setup.SETUP['url'])
  api = twitter.Api(username=username, password=password)
  api.PostUpdate('Release %(version)s of %(name)s is available from %(url)s' % metadata)
  print 'Done announcing on twitter.'
