# -*- coding: utf-8 -*-
# This file is part of Dyko
# Copyright © 2008-2010 Kozea
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Kalamar.  If not, see <http://www.gnu.org/licenses/>.

"""
Rest test.

Test the Restructured text backend.

"""

import tempfile
import shutil

from nose.tools import eq_
from kalamar.access_point.filesystem import FileSystem, FileSystemProperty
from kalamar.access_point.xml.rest import Rest, RestProperty
from kalamar.value import to_unicode
from ..common import run_common, make_site, require



class TemporaryDirectory(object):
    """Utility class for the tests."""
    def __init__(self):
        self.directory = None

    def __enter__(self):
        self.directory = tempfile.mkdtemp()
        return self.directory

    def __exit__(self, exit_type, value, traceback):
        shutil.rmtree(self.directory)


@require("docutils")
@require("lxml")
def make_file_ap(temp_dir):
    """Make filesystem access point."""
    return FileSystem(
        temp_dir, "(.*)\.txt", [("id", FileSystemProperty(int))],
        content_property="stream")

@require("docutils")
@require("lxml")
def test_serialization():
    """Test ReST serialization."""
    def xml_content_test(site):
        """Inner function to test ReST serialization."""
        item = site.open("things", {"id": 1})
        eq_(to_unicode(item["stream"].read()), to_unicode("===\nfoo\n==="))
    runner(xml_content_test)


# Common tests

def runner(test):
    """Test runner for ``test``."""
    with TemporaryDirectory() as temp_dir:
        file_access_point = make_file_ap(temp_dir)
        access_point = Rest(file_access_point, [
                ("name", RestProperty(unicode, "//title"))], "stream")
        site = make_site(access_point, fill=not hasattr(test, "nofill"))
        test(site)

@run_common
@require("docutils")
@require("lxml")
def test_rest_common():
    """Define a custom test runner for the common tests."""
    return None, runner, "ReST"
