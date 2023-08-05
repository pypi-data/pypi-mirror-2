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

"""Creates a debian package assuming the following:

  ./debian/  contains correct debian configuration files
  ./dist/<package>-<ver>-tar.gz has a built source package.

If a there's a ./tmp directory it'll blow it away and create a new one.

Outputs the final package to ./debian-<debversion>/ (ex. ./debian-squeeze/sid)

On any error it's exit.
"""

import os
import re
import shutil
import subprocess
import sys

def _CopyDir(from_dir, to_dir):
  """Recursively copy all the files from `from_dir` and below to `to_dir`."""
  print 'Copying from %r to %r' % (from_dir, to_dir)
  os.makedirs(to_dir)
  for fname in os.listdir(from_dir):
    from_name = os.path.join(from_dir, fname)
    if os.path.isdir(from_name):
      _CopyDir(from_name, os.path.join(to_dir, fname))
    else:
      shutil.copy2(from_name, to_dir)


def _CopyDebFileToDist(from_dir):
  """Copy the only .deb file to dist."""
  dest_dir = 'dist'
  for fname in os.listdir(from_dir):
    from_name = os.path.join(from_dir, fname)
    if os.path.isfile(from_name) and from_name.endswith('.deb'):
      shutil.copy(from_name, dest_dir)
      print 'Copied %r to %r' % (fname, dest_dir)
      return


def _MoveTopFilesToDir(from_dir, to_dir):
  """Copy top level files (only) in `from_dir` to `to_dir`."""
  os.makedirs(to_dir)
  for fname in os.listdir(from_dir):
    from_name = os.path.join(from_dir, fname)
    if os.path.isfile(from_name):
      shutil.move(from_name, to_dir)
  print 'Moved files to %r' % to_dir


def _RunOrDie(args, output=True):
  """Run the `args` (a list) or dies."""
  if output:
    print ' '.join(args)
  ret = subprocess.call(args)
  if ret:
    print 'Error running: %r' % ' '.join(args)
    sys.exit(-1)


def BuildDeb(setup):
  tmpdir = 'tmp'
  shutil.rmtree(tmpdir, True)
  dest_dir = '%s-%s' % (setup.NAME, setup.VER)
  dest_tar = '%s_%s' % (setup.NAME, setup.VER)
  _CopyDir('debian', os.path.join(tmpdir, dest_dir, 'debian'))

  src_tarname = dest_dir + '.tar.gz'
  dest_tarname = dest_tar + '.tar.gz'
  os.symlink(os.path.abspath(os.path.join('dist', src_tarname)),
             os.path.abspath(os.path.join(tmpdir, dest_tarname)))

  dest_tarname = dest_tar + '.orig.tar.gz'
  os.symlink(os.path.abspath(os.path.join('dist', src_tarname)),
             os.path.abspath(os.path.join(tmpdir, dest_tarname)))

  args = ['tar', '-zx', '--directory', tmpdir, '-f',
          os.path.join('dist', dest_dir + '.tar.gz')]
  _RunOrDie(args)
  old_cwd = os.getcwd()
  os.chdir(os.path.join(tmpdir, dest_dir))
  args = ['debuild',
      '--lintian-opts', '--info', '--display-info', '--display-experimental',
      '--color', 'always',
      #'--pedantic'
      #'--fail-on-warnings',
      ]
  _RunOrDie(args)
  os.chdir(old_cwd)
  # Move
  if os.path.exists('/etc/debian_version'):
    deb_ver = open('/etc/debian_version').read().rstrip()
  else:
    deb_ver = 'UNKNOWN'
  debdir='debian-%s' % deb_ver
  shutil.rmtree(debdir, True)
  _CopyDebFileToDist(tmpdir)
  _MoveTopFilesToDir(tmpdir, debdir)

  # Cleanup
  shutil.rmtree(tmpdir, True)
