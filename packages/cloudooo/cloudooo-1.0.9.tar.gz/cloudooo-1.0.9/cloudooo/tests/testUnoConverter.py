##############################################################################
#
# Copyright (c) 2009-2010 Nexedi SA and Contributors. All Rights Reserved.
#                    Gabriel M. Monnerat <gabriel@tiolive.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
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

import unittest
import jsonpickle
import pkg_resources
from subprocess import Popen, PIPE
from os.path import exists, join
from cloudoooTestCase import cloudoooTestCase, make_suite
from cloudooo.application.openoffice import openoffice
from cloudooo.document import FileSystemDocument


class TestUnoConverter(cloudoooTestCase):
  """Test case to test all features of the unoconverter script"""

  file_msg_list = ["Microsoft Office Document",
                  "CDF V2 Document, Little Endian, Os: Windows, Version 1.0,"]

  def afterSetUp(self):
    """ """
    openoffice.acquire()
    self.hostname, self.port = openoffice.getAddress()
    data = open("data/test.odt", 'r').read()
    self.document = FileSystemDocument(self.tmp_url, data, 'odt')

  def tearDown(self):
    """Called to unlock the openoffice"""
    openoffice.release()

  def testUnoConverterOdtToDoc(self):
    """Test script unoconverter"""
    mimemapper = dict(filter_list=[('doc', 
                                    'com.sun.star.text.TextDocument',
                                    'MS Word 97')],
                     doc_type_list_by_extension=dict(doc=['com.sun.star.text.TextDocument']))
    jsonpickle_path = "/".join(pkg_resources.resource_filename("jsonpickle",
                                     "").split("/")[:-1])
    mimemapper_pickled = jsonpickle.encode(mimemapper)
    command = [join(self.office_binary_path, "python"),
          pkg_resources.resource_filename("cloudooo", 
                                          "helper/unoconverter.py"),
          "'--convert'",
          "--uno_path='%s'" % self.uno_path,
          "--office_binary_path='%s'" % self.office_binary_path,
          "--hostname='%s'" % self.hostname,
          "--port='%s'" % self.port,
          "--document_url='%s'" % self.document.getUrl(),
          "--destination_format='%s'" % "doc",
          "--source_format='%s'" % "odt",
          "--mimemapper='%s'" % mimemapper_pickled,
          "--jsonpickle_path='%s'" % jsonpickle_path]
    stdout, stderr = Popen(' '.join(command), shell=True, 
        stdout=PIPE, stderr=PIPE).communicate()
    self.assertEquals(stderr, '')
    output_url = stdout.replace('\n', '')
    self.assertEquals(exists(output_url), True, stdout)
    stdout, stderr = Popen("file %s" % output_url, shell=True, 
        stdout=PIPE, stderr=PIPE).communicate()
    self.assertEquals(self.file_msg_list[1] in stdout \
                      or \
                      self.file_msg_list[0] in stdout,
                      True,
                      "%s don't have %s" % (self.file_msg_list, stdout))
    self.document.trash()
    self.assertEquals(exists(output_url), False)


def test_suite():
  return make_suite(TestUnoConverter)

if __name__ == "__main__":
  from cloudoooTestCase import startFakeEnvironment, stopFakeEnvironment
  startFakeEnvironment()
  suite = unittest.TestLoader().loadTestsFromTestCase(TestUnoConverter)
  unittest.TextTestRunner(verbosity=2).run(suite)
  stopFakeEnvironment()
