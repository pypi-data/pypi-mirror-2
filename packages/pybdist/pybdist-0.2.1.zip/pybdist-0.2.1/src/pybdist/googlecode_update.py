#!/usr/bin/env python
#
# Copyright 20l0 Google Inc. All Rights Reserved.
#
# Script for downloading file information from a Google Code project.
#
# Note that the upload script requests that you enter your
# googlecode.com password.  This is NOT your Gmail account password!
# This is the password you use on googlecode.com for committing to
# Subversion and uploading files.  You can find your password by going
# to http://code.google.com/hosting/settings when logged in with your
# Gmail account. If you have already committed to your project's
# Subversion repository, the script will automatically retrieve your
# credentials from there (unless disabled, see the output of '--help'
# for details).

import urllib2
import httplib
import re
import os
import base64

def get_document_list(project_name):
  url = 'http://code.google.com/feeds/p/%s/downloads/basic' % project_name
  f = urllib2.urlopen(url)
  text = f.read()
  f.close()
  re_entry = re.compile(r'<entry>(.+?)</entry>', re.DOTALL)

  list = []
  for match in re_entry.finditer(text):
    entry = match.group(1)
    updated = re.search(r'<updated>(.+?)</updated>', entry).group(1)
    title = re.search(r'<title>\s*(.*)\s*</title>', entry).group(1)
    labels = re.search(r'Labels:(.+?)&lt;', entry, re.DOTALL).group(1)
    labels = labels.split()
    fname = re.search(r'downloads/detail\?name=(.+?)"', entry).group(1)
    list.append(dict(updated=updated, title=title, labels=labels, fname=fname))

  return list


def get_last_versions(project_name):
  lst = get_document_list(project_name)
  sort(lst)


def update_labels(fname, project_name, user_name, password, labels):
  if user_name.endswith('@gmail.com'):
    user_name = user_name[:user_name.index('@gmail.com')]

  form_fields = [
      ('_charset_', ''),
      ('projectname', project_name),
      ('summary', fname),
      ('filename', fname),
      ]
  if labels is not None:
    form_fields.extend([('label', l.strip()) for l in labels])
  for n in range(15 - len(labels)):
    form_fields.append(('label', ''))
  form_fields.append(('btn', 'Save changes'))
  content_type, body = encode_upload_request(form_fields)

  upload_host = 'code.google.com'
  upload_uri = '/p/%s/downloads/update.do?name=%s' % (project_name, fname)
  auth_token = base64.b64encode('%s:%s'% (user_name, password))
  headers = {
    'Authorization': 'Basic %s' % auth_token,
    'User-Agent': 'Googlecode.com updater v0.1.0',
    'Content-Type': content_type,
    }
  server = httplib.HTTPConnection(upload_host)
  print upload_host, upload_uri
  print body
  print headers
  server.request('POST', upload_uri, body, headers)
  resp = server.getresponse()
  print resp.read()
  server.close()

  if resp.status == 201:
    location = resp.getheader('Location', None)
  else:
    location = None
  return resp.status, resp.reason, location


def update_status(project_name, fname, user_name, password, labels):
  status, reason, url = update_labels(fname, project_name, user_name, password,
                                      labels)

  # Returns 403 Forbidden instead of 401 Unauthorized for bad
  # credentials as of 2007-07-17.
  if status in [httplib.FORBIDDEN, httplib.UNAUTHORIZED]:
    print 'First:', status, reason
  else:
    print status, reason
    return


def encode_upload_request(fields):
  """Encode the given fields and file into a multipart form body.

  fields is a sequence of (name, value) pairs. file is the path of
  the file to upload. The file will be uploaded to Google Code with
  the same file name.

  Returns: (content_type, body) ready for httplib.HTTP instance
  """
  BOUNDARY = '----------Googlecode_boundary_reindeer_flotilla'
  CRLF = '\r\n'

  body = []

  # Add the metadata about the upload first
  for key, value in fields:
    body.extend(
      ['--' + BOUNDARY,
       'Content-Disposition: form-data; name="%s"' % key,
       '',
       value,
       ])

  # Finalize the form body
  body.extend(['--' + BOUNDARY + '--', ''])

  return 'multipart/form-data; boundary=%s' % BOUNDARY, CRLF.join(body)

if __name__ == '__main__':
  get_document_list('pybdist')
  pwd = open(os.path.expanduser('~/.ssh/scott@forusers.com')).read().strip()
  update_status('pybdist', 'pybdist-0.1.2.zip', 'scott@forusers.com', pwd,
      ['Type-Source', 'OpSys-Linux', 'Featured'])

