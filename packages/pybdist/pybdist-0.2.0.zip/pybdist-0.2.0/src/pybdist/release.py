#!/usr/bin/python
# -*- coding: utf-8 -*-
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

"""Parses a release file and gets the latest release information.
Code assumes that the release has a date and a version.
And sections are separated by ======== or --------
"""

import os
import re
import sys
import urllib2


def ParseLastRelease(fname, pattern):
  """Parse the last release in an RST release file.
  Args:
    fname: filename
    pattern: Regular expression or null, expects the <date> and <ver> groups.
  Returns:
    (version, date, lines)
  """
  # Example "Apr. 18th, 2009 v 0.16"
  if not pattern:
    pattern = r'(?P<date>.*) v (?P<ver>\d+.\d+(?:.\d+)?)$'

  re_version = re.compile(pattern)
  re_horz = re.compile(r'^[-=]+$')
  version = None
  lines = []
  for line in open(fname):
    line = line.rstrip()
    grps = re_version.match(line)
    if grps:
      if version:
        break;
      date, version = grps.group('date'), grps.group('ver')
    elif re_horz.match(line):
      pass
    elif version:
      lines.append(line)

  if not lines:
    print 'No line with %r pattern found in %r' % (pattern, fname)
    sys.exit(-1)

  if not lines[-1]:
    del lines[-1]

  return version, date, lines


def ParseDebChangelog(fname):
  re_ver = re.compile(r'^[\w-]+ \(([^)]+)\) ')
  re_date = re.compile(r'^ -- [\w ]+ <[^>]>  (.*)')
  version = None
  date = None
  lines = []
  for line in file('debian/changelog'):
    line = line.rstrip()
    grps = re_ver.search(line)
    if grps:
      version = grps.group(1)
      continue
    grps = re_date.search(line)
    if grps:
      date = grps.group(1)
      break
    if version and line:
      lines.append(line)
  n = version.rfind('-')
  if n != -1:
    version = version[:n]
  return version, date, lines

def SafeGetGroup(regex, haystack, opts=0):
  """Get's group 1 or '' if it doesn't exist."""
  grps = re.search(regex, haystack, opts)
  if grps:
    return grps.group(1)
  return ''

def GetDocumentList(project_name):
  url = 'http://code.google.com/feeds/p/%s/downloads/basic' % project_name
  print 'Fetching %r' % url
  f = urllib2.urlopen(url)
  text = f.read()
  f.close()
  re_entry = re.compile(r'<entry>(.+?)</entry>', re.DOTALL)

  list = []
  for match in re_entry.finditer(text):
    entry = match.group(1)
    updated = SafeGetGroup(r'<updated>(.+?)</updated>', entry)
    title = SafeGetGroup(r'<title>\s*(.*)\s*</title>', entry)
    labels = SafeGetGroup(r'Labels:(.+?)&lt;', entry, re.DOTALL)
    labels = labels.split()
    fname = SafeGetGroup(r'downloads/detail\?name=(.+?)"', entry)
    list.append(dict(updated=updated, title=title, labels=labels, fname=fname))

  return list


def _GetLastVersions(project_name):
  versions = []
  re_version = re.compile(r'%s-(.*).tar.gz' % project_name)
  for v in GetDocumentList(project_name):
    grps = re_version.search(v['fname'])
    if grps:
      ver = grps.group(1)
      versions.append((v['updated'], ver, [v['title']]))
  return versions


def GetLastGoogleCodeVersion(project_name):
  versions = _GetLastVersions(project_name)
  if not versions:
    return (None, None, None)
  versions.sort()
  last = versions[-1]
  return last[1], last[0], last[2]


def RstExperiment():
  import docutils
  import docutils.utils
  from docutils.parsers.rst import Parser
  from docutils import core

  fname = 'RELEASE.rst'
  overrides = {'input_encoding': 'unicode',
               'doctitle_xform': 1,
               'initial_header_level': 1}
  lines = []
  for line in open(fname):
    lines.append(unicode(line))

  document = core.publish_doctree(
      source=u'\n'.join(lines), source_path=fname,
      settings_overrides=overrides)

  parts = core.publish_parts(
      source=u'\n'.join(lines), source_path=fname,
      destination_path=None,
      writer_name='html', settings_overrides=overrides)
  body = parts['html_body']
  print body


if __name__ == '__main__':
  ver, date, lines = ParseLastRelease('RELEASE.rst')
  print ver, date, lines
