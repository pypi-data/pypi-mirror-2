#!/usr/bin/python
# Copyright 2010 Scott Kirkwood. All Rights Reserved.

"""Build a debian package.

I believe you'll need:
 sudo apt-get install debianutils lintian

Much of this code was copied and pasted from TaskCoach a great program.
by Frank Niessink <frank@niessink.com>
"""

import glob
import os
import shutil
import sys
import tarfile
import textwrap
import time, glob

from distutils.core import Command
from distutils import log, errors
from distutils.file_util import copy_file, move_file

class bdist_deb(Command, object):
  description = 'create a Debian (.deb) package'

  user_options = [
      ('sdist=', None, 'Source distribution .tar.gz archive'),
      ('bdist-base=', None,
       'base directory for creating built distributions [build]'),
      ('dist-dir=', 'd', 'directory to put final deb files in [dist]'),
      ('package=', None, 'package name of the application'),
      ('section=', None, 'section of the menu to put the application in [Applications]'),
      ('subsection=', None, 'subsection of the menu to put the application in'),
      ('title=', None, 'title of the application'),
      ('description=', None, 'brief single line description of the application'),
      ('long-description=', None, 'long description of the application'),
      ('version=', None, 'version of the application'),
      ('package-version=', None, 'version of the package [1]'),
      ('distribution=', None, 'distribution of the package [UNRELEASED]'),
      ('command=', None, 'command to start the application'),
      ('priority=', None, 'priority of the deb package [optional]'),
      ('urgency=', None, 'urgency of the deb package [low]'),
      ('maintainer=', None, 'maintainer of the deb package [<author>]'),
      ('maintainer-email=', None, 'email address of the package maintainer [<author-email>]'),
      ('author=', None, 'author of the application'),
      ('author-email=', None, 'email address of the application author'),
      ('copyright=', None, 'copyright notice of the application'),
      ('license=', None, 'license (title and version) of the application'),
      ('license-abbrev=', None, 'abbreviated license title, e.g. "GPLv3"'),
      ('license-summary=', None, 'summary of the license of the application'),
      ('license-path=', None, 'path of the license on Debian systems'),
      ('url=', None, 'url of the application homepage'),
      ('architecture=', None, 'architecure of the deb package [all]'),
      ('man-src=', None, 'Where to find the man dir.'),
      ('icon=', None, 'Icon to use.'),
      ('desktop-file=', None, '.desktop file to use.'),
      ('depends=', None, 'list of dependancies')]

  def initialize_options(self):
    self.bdist_base = 'build'
    self.dist_dir = 'dist'
    self.section = 'Applications'
    self.priority = 'optional'
    self.urgency = 'low'
    self.architecture = 'all'
    self.debs_final = []
    self.sdist = self.package = self.subsection = self.title = \
        self.description = self.long_description = self.command = \
        self.maintainer = self.maintainer_email = self.author = \
        self.author_email = self.copyright = self.license = \
        self.license_abbrev = self.license_summary = self.license_path = \
        self.url = self.version = self.package_version = \
        self.distribution = self.man_src = self.icon = self.desktop_file = \
        self.depends = None

  def finalize_options(self):
    mandatoryOptions = [\
        ('package', 'the package name'),
        ('title', 'a title for the menu'),
        ('description', 'a brief description for the menu'),
        ('long_description', 'a long description of the application'),
        ('version', 'the version of the application'),
        ('copyright',
         'a copyright description ("Copyright year-year, author")'),
        ('license', 'the title (including version) of the license'),
        ('license_abbrev', 'an abbreviated license title'),
        ('license_summary', 'a summary of the license of the application'),
        ('license_path', 'the path of the license on Debian systems'),
        ('author', 'the author of the application'),
        ('author_email', 'the email address of the author'),
        ('url', 'the url of the application homepage')]
    for option, description in mandatoryOptions:
      if not getattr(self, option):
        raise errors.DistutilsOptionError, \
            'you must provide %s (--%s)' % (description, option)
    if not self.maintainer:
      self.maintainer = self.author
      self.maintainer_email = self.author_email
    if not self.package_version:
      self.package_version = ''
    else:
      self.package_version = '-%s' % self.package_version
    if not self.distribution:
      self.distribution = 'UNRELEASED'
    if self.subsection:
      self.subsection_lower = self.subsection.lower()
    else:
      self.subsection_lower = 'python'
    self.datetime = time.strftime('%a, %d %b %Y %H:%M:%S +0000',
                                  time.gmtime())
    self.year = time.gmtime()[0]
    self.license_summary = self.wrap_paragraphs(self.license_summary,
                                                indent='    ')
    self.long_description = self.wrap_paragraphs(self.long_description,
                                                 indent=' ')
    if self.man_src:
      self.man_rule = '\tdh_installman -p%s %s\n' % (self.package, self.man_src)
    else:
      self.man_rule = ''
    if self.desktop_file:
      self.desktop_install = '\tdh_install -p%s %s /usr/share/applications/\n' % (self.package,
          self.desktop_file)
    else:
      self.desktop_install = ''
    if self.subsection:
      self.section_rule = '  section="%s/%s"\\\n' % (self.section, self.subsection)
    else:
      self.section_rule = ''
    if self.icon:
      self.icon_rule = '  icon="/usr/share/pixmaps/%s"\\\n' % os.path.basename(self.icon)
      self.icon_install = '\tdh_install -p%s tmp/%s %s\n' % (self.package,
          os.path.basename(self.icon), '/usr/share/pixmaps/')
    else:
      self.icon_rule = ''
      self.icon_install = ''

  def run(self):
    self.copy_sdist()
    self.untar_sdist()
    self.create_debian_dir()
    self.write_debian_files()
    self.build_debian_package()
    self.run_lintian()
    self.move_debian_package_to_distdir()

  def copy_sdist(self):
    """ Copy the source distribution (.tar.gz archive) to the build dir. """
    if not os.path.isdir(self.bdist_base):
      os.mkdir(self.bdist_base)
    (dest_name, copied) = copy_file(self.sdist, self.bdist_base)
    orig_name = self.get_orig_tar_name()
    if os.path.exists(orig_name):
      os.remove(orig_name)
    self.sdist_archive = move_file(dest_name, orig_name)

  def get_orig_tar_name(self):
    orig_name = os.path.join(self.bdist_base, self.package + '_' + self.version + '.orig.tar.gz')
    orig_name = orig_name.lower()
    orig_name = orig_name.replace('-', '_')
    return orig_name

  def untar_sdist(self):
    """ Unzip and extract the source distribution archive. """
    expected_extracted_dir = self.sdist_archive[:-len('.orig.tar.gz')] + '/'
    if self.verbose:
      log.info('extracting %s to %s'%(self.sdist_archive,
                                        expected_extracted_dir))
    archive = tarfile.open(self.sdist_archive)
    extracted_dir = os.path.join(self.bdist_base, archive.getnames()[0])
    archive.extractall(self.bdist_base)
    archive.close()
    if expected_extracted_dir != extracted_dir:
      if os.path.exists(expected_extracted_dir):
        shutil.rmtree(expected_extracted_dir)
      os.rename(extracted_dir, expected_extracted_dir)
    self.extracted_dir = expected_extracted_dir

  def create_debian_dir(self):
    """ Create the debian dir for package files. """
    self.debian_dir = os.path.join(self.extracted_dir, 'debian')
    if self.verbose:
        log.info('creating %s'%self.debian_dir)
    os.mkdir(self.debian_dir)

  def write_debian_files(self):
    """ Create the different package files in the debian folder. """
    debian_files = dict(rules=rules, compat='5\n', pycompat='2\n',
        menu=menu, control=control, copyright=self.copyright_contents(),
        changelog=changelog, pyversions=pyversions)
    if not self.subsection or not self.command:
      del debian_files['menu']
    for filename, contents in debian_files.iteritems():
      self.write_debian_file(filename, contents%self.__dict__)
    if self.icon:
      self.copy_debian_file(self.icon, 'tmp')

  def write_debian_file(self, filename, contents):
    filename = os.path.join(self.debian_dir, filename)
    if self.verbose:
      log.info('writing %s', filename)
    fd = file(filename, 'w')
    fd.write(contents)
    fd.close()
    os.chmod(filename, 0755)

  def copy_debian_file(self, from_file, to_dir):
    to_dir = os.path.join(self.extracted_dir, to_dir)
    if not os.path.isdir(to_dir):
      print 'Creating dir %r' % to_dir
      os.makedirs(to_dir)
    (dest_name, copied) = copy_file(from_file, to_dir)
    if not copied:
      print 'Unable to copy file %r to %r' % (from_file, to_dir)
      sys.exit(-1)
    os.chmod(dest_name, 0644)

  def build_debian_package(self):
    curdir = os.getcwd()
    os.chdir(self.extracted_dir)
    ret = os.system('debuild -i -S')
    if ret:
      print 'debuild -S had an error: quitting.'
      sys.exit(-1)
    ret = os.system('dpkg-buildpackage -rfakeroot')
    if ret:
      print 'dpkg-buildpackage returned with an error: quitting.'
      sys.exit(-1)
    os.chdir(curdir)

  def run_lintian(self):
    for deb_package in glob.glob('build/*.deb'):
      print 'Running lintian in %r' % deb_package
      ret = os.system('lintian --check --info --display-info %s' % deb_package)
      if ret:
        print 'lintian returned with an error: quitting.'
        sys.exit(-1)

  def move_debian_package_to_distdir(self):
    self.debs_final = []
    for deb_package in glob.glob('build/*.deb'):
      self.debs_final.append(move_file(deb_package, self.dist_dir))

  def copyright_contents(self):
    """ Create copyright contents. This is a bit complicated because the
        header and footer need to have their variables filled in first
        before their text can be wrapped. """
    return self.wrap_paragraphs(copyright_header%self.__dict__) + \
        copyright + self.wrap_paragraphs(copyright_footer%self.__dict__)

  def wrap_paragraphs(self, text, indent=''):
    paragraphs = text.split('\n\n')
    paragraphs = ['\n'.join(textwrap.wrap(paragraph, width=76,
                  initial_indent=indent, subsequent_indent=indent)) \
                  for paragraph in paragraphs]
    return '\n\n'.join(paragraphs)


rules = """#!/usr/bin/make -f

DEB_PYTHON_SYSTEM := pysupport

include /usr/share/cdbs/1/rules/debhelper.mk
include /usr/share/cdbs/1/class/python-distutils.mk

# Don't compress .py files
DEB_COMPRESS_EXCLUDE := .py

binary-install/%(package)s::
\tdh_icons
%(man_rule)s%(icon_install)s%(desktop_install)s"""

pyversions = """2.4-"""

menu = """?package(%(package)s):needs="X11"\\
  title="%(title)s"\\
  description="%(description)s"\\
  hints="Gnome"\\
  command="%(command)s"\\
%(icon_rule)s%(section_rule)s
"""

control = """Source: %(package)s
Section: %(subsection_lower)s
Priority: %(priority)s
Maintainer: %(maintainer)s <%(maintainer_email)s>
Build-Depends: cdbs (>= 0.4.49), debhelper (>= 7), python (>= 2.4), python-support
Standards-Version: 3.8.4
Homepage: %(url)s

Package: %(package)s
Architecture: %(architecture)s
Depends: ${misc:Depends}, ${python:Depends}, %(depends)s
Description: %(description)s
%(long_description)s
"""

copyright_header = """This package was debianized by %(maintainer)s
<%(maintainer_email)s> on %(datetime)s.
"""

copyright = """

It was downloaded from %(url)s

Upstream Author:

    %(author)s <%(author_email)s>

Copyright:

    %(copyright)s

License:

%(license_summary)s

"""

copyright_footer = """On Debian systems, the complete text of the %(license)s
can be found in '%(license_path)s'.

The Debian packaging is Copyright %(year)s, %(maintainer)s <%(maintainer_email)s> and
is licensed under the %(license_abbrev)s, see above.

"""

changelog = """%(package)s (%(version)s%(package_version)s) %(distribution)s; urgency=%(urgency)s

  * New upstream release.

 -- %(maintainer)s <%(maintainer_email)s>  %(datetime)s
"""
