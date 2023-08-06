#! /usr/bin/python
##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
#                    Yoshinori Okuji <yo@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################


"""Generate repository information on Business Templates.
"""

import tarfile
import os
import os.path
import sys
import tempfile
import shutil
import cgi

property_list = '''
title
version
revision
description
license
dependency_list
provision_list
copyright_list
'''.strip().splitlines()

bt_title_path = os.path.join('bt', 'title')

def info(message):
  """Print a message to stdout.
  """
  sys.stdout.write(message)

def err(message):
  """Print a message to stderr.
  """
  sys.stderr.write(message)

def readProperty(property_dict, property_name, property_file):
    try:
      text = property_file.read()
      if property_name.endswith('_list'):
        property_dict[property_name[:-5]] = text and text.split('\n') or []
      else:
        property_dict[property_name] = text
    finally:
      property_file.close()

def readBusinessTemplate(tar):
  """Read an archived Business Template info.
  """
  property_dict = {}
  for info in tar:
    name_list = info.name.split('/')
    if len(name_list) == 3 and name_list[1] == 'bt' and name_list[2] in property_list:
      property_file = tar.extractfile(info)
      property_name = name_list[2]
      readProperty(property_dict, property_name, property_file)

  return property_dict

def readBusinessTemplateDirectory(dir):
  """Read Business Template Directory info.
  """
  property_dict = {}
  for property_name in property_list:
    filename = os.path.join(dir, 'bt', property_name)
    if os.path.isfile(filename):
      property_file = open(filename, 'rb')
      readProperty(property_dict, property_name, property_file)

  return property_dict

def generateInformation(fd):
  os.write(fd, '<?xml version="1.0"?>\n')
  os.write(fd, '<repository>\n')

  for file in sorted(os.listdir(os.getcwd())):
    if file.endswith('.bt5'):
      info('Reading %s... ' % (file,))
      try:
        tar = tarfile.open(file, 'r:gz')
      except tarfile.TarError:
        err('An error happened in %s; skipping\n' % (file,))
        continue
      try:
        property_dict = readBusinessTemplate(tar)
      finally:
        tar.close()
    elif os.path.isfile(os.path.join(file, bt_title_path)):
      info('Reading Directory %s... ' % (file,))
      property_dict = readBusinessTemplateDirectory(file)
    else:
      continue
    property_id_list = property_dict.keys()
    property_id_list.sort()
    os.write(fd, '  <template id="%s">\n' % (file,))
    for property_id in property_id_list:
      property_value = property_dict[property_id]
      if type(property_value) == type(''):
        os.write(fd, '    <%s>%s</%s>\n' % (
              property_id, cgi.escape(property_value), property_id))
      else:
        for value in property_value:
          os.write(fd, '    <%s>%s</%s>\n' % (
                property_id, cgi.escape(value), property_id))
    os.write(fd, '  </template>\n')
    info('done\n')
  os.write(fd, '</repository>\n')

def main():
  if len(sys.argv) < 2:
    dir_list = ['.']
  else:
    dir_list = sys.argv[1:]

  _main(dir_list)

def _main(dir_list=["."]):
  cwd = os.getcwd()
  for d in dir_list:
    os.chdir(d)
    fd, path = tempfile.mkstemp()
    try:
      try:
        generateInformation(fd)
      finally:
        os.close(fd)
    except:
      os.remove(path)
      raise
    else:
      shutil.move(path, 'bt5list')
      cur_umask = os.umask(0666)
      os.chmod('bt5list', 0666 & ~cur_umask)
      os.umask(cur_umask)
    os.chdir(cwd)

if __name__ == "__main__":
  main()
