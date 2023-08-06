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
Heterogeneous view test.

Test an heterogeneous view on a memory and an alchemy access point.

"""

import unittest
from nose.tools import eq_

from kalamar.access_point.alchemy import AlchemyProperty, Alchemy
from kalamar.access_point.memory import Memory
from kalamar.site import Site
from kalamar.property import Property
from kalamar.item import Item
from .common import require



def make_alchemy_ap():
    """Build an alchemy access point referencing another access point."""
    id_property = AlchemyProperty(int, column_name="id")
    label = AlchemyProperty(unicode, column_name="label")
    memory = AlchemyProperty(
        Item, column_name="memory", relation="many-to-one",
        remote_ap="memory")
    access_point = Alchemy(
        "sqlite:///", "test_heterogeneous",
        {"id": id_property, "label": label, "memory": memory},
        ["id"], True)
    return access_point

def make_memory_ap():
    """Build a memory access point referenced by another access_point."""
    access_point = Memory(
        {"id": Property(int), "label": Property(unicode)}, ("id",))
    return access_point


@require("sqlalchemy")
class TestHeterogeneous(unittest.TestCase):
    """Test class testing ``view`` over different access points."""
    def test_view(self):
        """Test the ``view`` method across access points."""
        aliases = {
            "alch_id": "id", "alch_label": "label", "mem_id": "memory.id",
            "mem_label": "memory.label"}
        items = list(self.site.view("alchemy", aliases, {}))
        eq_(len(items), 1)
        item = items[0]
        eq_(item["alch_id"], 1)
        eq_(item["alch_label"], "alchemytest")
        eq_(item["mem_id"], 1)
        eq_(item["mem_label"], "memorytest")

    # camelCase function names come from unittest
    # pylint: disable=C0103
    def setUp(self):
        self.site = Site()
        self.alchemy_ap = make_alchemy_ap()
        self.site.register("alchemy", self.alchemy_ap )
        self.site.register("memory", make_memory_ap())
        self.memitem = self.site.create(
            "memory", {"id": 1, "label": "memorytest"})
        self.memitem.save()
        self.dbitem = self.site.create(
            "alchemy",
            {"id": 1, "label": "alchemytest", "memory": self.memitem})
        self.dbitem.save()

    def tearDown(self):
        self.alchemy_ap._table.drop()
        Alchemy.__metadatas = {}
    # pylint: enable=C0103
