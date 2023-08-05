#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Scott Kirkwood. All Rights Reserved.
"""

You'll need:
sudo aptitude install alien help2man fakeroot
"""

__author__ = 'Scott Kirkwood (scott+pybdist@forusers.com)'
__version__ = '0.1.1'

import codecs
import distutils.core
import getpass
import glob
import googlecode_upload as gup
import httplib
import netrc
import os
import re
import release
import shutil
import simplejson
import subprocess
import sys

import bdist_deb

def GetVersion(setup):
  fname = '%s/%s' % (setup.DIR, setup.PY_SRC)
  re_py_ver = re.compile(r'__version__\s*=\s*[\'"](.*)[\'"]')
  grps = re_py_ver.search(open(fname).read())
  source_ver = grps.group(1)

  setup_ver = setup.VER
  if setup_ver != source_ver:
    print 'Setup versions dissagree'
    print '%s = %r' % (setup.PY_SRC, source_ver)
    print 'setup.py = %r' % setup_ver
    print 'Please fix this before continuing'
    sys.exit(-1)

  rel_ver, rel_date, rel_lines = release.ParseLastRelease(setup.RELEASE_FILE)
  if rel_ver != setup_ver:
    print 'Need to update the %r, version %r doesn\'t match %r' % (setup.RELEASE_FILE,
       rel_ver, setup_ver)
    sys.exit(-1)

  print 'Setup versions agree'
  return setup_ver

def ParseLastRelease(setup):
  _, rel_date, rel_lines = release.ParseLastRelease(setup.RELEASE_FILE)
  return rel_date, rel_lines

def BuildZipTar(unused_setup):
  subprocess.call([
    'python', 'setup.py', 'sdist', '--formats=gztar,zip'])
  print 'Built zip and tar'


def UploadToPyPi(unused_setup):
  subprocess.call([
    'python', 'setup.py', 'sdist', '--formats=zip', 'upload',])
  print 'Upload to pypi'


def BuildMan(setup):
  if not setup.MAN_FILE:
    return
  try:
    dest_dir = os.path.dirname(setup.MAN_FILE)
    if not os.path.isdir(dest_dir):
      os.makedirs(dest_name)
    include_file = setup.MAN_FILE.replace('.1', '.include')
    subprocess.call([
      'help2man',
      '%s/%s' % (setup.DIR, setup.PY_SRC),
      #'%s' % setup.NAME,
      '-N', # no pointer to TextInfo
      '-i', include_file,
      '-o', dest_name])

    print 'Built %s.1' % setup.NAME
  except Exception, e:
    print 'You may need to install help2man', e
    sys.exit(-1)


def BuildDeb(setup):
  sys.argv = [sys.argv[0], 'bdist_deb', '--sdist=dist/%s-%s.tar.gz' % (setup.NAME, setup.VER)]
  setup.SETUP.update(dict(
      cmdclass={'bdist_deb': bdist_deb.bdist_deb},
      options=dict(
        bdist_deb=dict(
          package=setup.DEB_NAME,
          title=setup.NAME,
          description=setup.SETUP['description'],
          long_description=setup.SETUP['long_description'],
          version=setup.VER,
          author=setup.AUTHOR_NAME,
          author_email=setup.SETUP['author_email'],
          copyright=setup.COPYRIGHT,
          license=setup.LICENSE_TITLE_AND_VERSION,
          license_abbrev=setup.LICENSE_TITLE_AND_VERSION_ABBREV,
          license_path=setup.LICENSE_PATH,
          license_summary=setup.LICENSE_NOTICE,
          subsection=setup.MENU_SUBSECTION,
          depends=','.join(setup.DEPENDS),
          url=setup.SETUP['url'],
          man_src=setup.MAN_FILE,
          command=setup.COMMAND))))
  distutils.core.setup(**setup.SETUP)
  GetDebFilenames(setup)
  print 'Built debian package'
  return


def GetDebFilenames(setup):
  debs = ['dist/%s_%s-1_all.deb' % (setup.DEB_NAME, setup.VER)]
  for deb in debs:
    if not os.path.exists(deb):
      print 'Missing debian file %s' % deb
      sys.exit(-1)

  return debs


def _CleanConfig(setup):
  config_file = os.path.expanduser('~/.config/%s/config' % setup.NAME)
  if os.path.exists(config_file):
    os.unlink(config_file)

def _CleanDoc(setup):
  docs = '/usr/share/doc/%s' % setup.NAME
  if os.path.exists(docs):
    print 'rm -r %s' % docs
    shutil.rmtree(docs)

def _CleanMan(setup):
  man = '/usr/share/man/man1/%s.1.gz' % setup.NAME
  if os.path.exists(man):
    print 'rm %s' % man

def _CleanScripts(setup):
  if 'scripts' not in setup.SETUP:
    return
  for script in setup.SETUP['scripts']:
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
  if not base_dir:
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
  _CleanConfig(setup)
  _CleanPackages(setup)
  _CleanDoc(setup)
  _CleanMan(setup)
  _CleanScripts(setup)


def _UploadToGoogleCode(project, fname, username, password):
  print 'Uploading %s' % fname
  summary = fname
  if fname.endswith('.zip') or fname.endswith('.tar.gz'):
    labels = ['Type-Source', 'OpSys-Linux', 'Featured']
  elif fname.endswith('.deb'):
    labels = ['Type-Package', 'OpSys-Linux', 'Featured']
  else:
    labels = None
  gup.upload('dist/%s' % fname, project, username, password, summary, labels)
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
  rel_ver, rel_date, rel_lines = release.ParseLastRelease(setup.RELEASE_FILE)
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
  release = dict(version=setup.VER, changelog='\n'.join(changelog), tag_list=tag)
  path = '/projects/%s/releases.json' % name
  body = codecs.encode(simplejson.dumps(dict(auth_code=auth_code, release=release)))
  connection = httplib.HTTPConnection('freshmeat.net')
  connection.request('POST', path, body, {'Content-Type': 'application/json'})
  response = connection.getresponse()
  if response.status != 201:
    print 'Request failed: %d %s' % (response.status, response.reason)
  print 'Done announcing on Freshmeat.'


