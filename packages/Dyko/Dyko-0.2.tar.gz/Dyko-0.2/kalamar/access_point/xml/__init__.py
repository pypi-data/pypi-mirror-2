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
XML
===

An access point designed to store properies in a XML file.

"""

from __future__ import print_function

try:
    from lxml import etree
except ImportError:
    import sys
    print("WARNING: The XML AP is not available.", file=sys.stderr)

from kalamar.access_point.decorator import Decorator, DecoratorItem, \
        DecoratorProperty
from kalamar.item import AbstractItem, Item
from kalamar.request import make_request, normalize

try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO


class XMLItem(DecoratorItem):
    """Base XML Item."""
    def __init__(self, access_point, wrapped_item, decorated_values=None):
        super(XMLItem, self).__init__(
            access_point, wrapped_item, decorated_values)
        self._xml_tree = None

    @property
    def xml_tree(self):
        """Return the XML tree parsed from the ``stream_property`` item."""
        if self._xml_tree is None:
            parser = etree.XMLParser()
            xmlstring = self[self.access_point.stream_property].read()
            if xmlstring == None or not xmlstring.strip():
                # Create a new xml tree if there isn't one
                root = etree.Element(self.access_point.root_element)
                self._xml_tree = etree.ElementTree(element=root)
            else:
                self._xml_tree = etree.fromstring(xmlstring, parser)
        return self._xml_tree


class XMLProperty(DecoratorProperty):
    """Property used with the XML access point."""
    def __init__(self, property_type, xpath, *args, **kwargs):
        super(XMLProperty, self).__init__(
            property_type, *args, **kwargs)
        self.xpath = xpath.strip("/")
        parts = self.xpath.split("/")
        self.tag_name = parts[-1]
        self.parent_xpath = "//" + "/".join(parts[:-1])

    def getter(self, item):
        if self.relation == "one-to-many":
            return self.access_point._default_loader({}, self)(item)
        nodes = self.get_nodes(item)
        if len(nodes) == 0:
            return (None,)
        elif self.type == Item:
            return self.item_from_xml(nodes[0])
        elif self.type == iter:
            return ((node.text for node in nodes),)
        return self.cast(tuple(node.text for node in nodes))

    def get_nodes(self, item):
        """Return the XML nodes associated to the properties."""
        nodes = item.xml_tree.xpath(self.xpath)
        return nodes

    def item_from_xml(self, elem):
        """Build an item from an element representing an item.

        Subclasses may override this method according to their XML
        serialization mechanism.

        """
        request_dict = dict(((child.tag, child.text) for child in elem))
        if request_dict:
            request = normalize(
                self.remote_ap.properties, make_request(request_dict))
            return (self.remote_ap.open(request),)
        else:
            return (None,)

    def to_xml(self, value):
        """Build an XML element for a given value."""
        def fill_elem(elem, value):
            """Inner function filling an element according to the value."""
            if isinstance(value, AbstractItem):
                identity = value.identity
                for name, value in identity.conditions.items():
                    subelement = etree.Element(name)
                    fill_elem(subelement, value)
                    elem.append(subelement)
            else:
                elem.text = value

        element = etree.Element(self.tag_name)
        fill_elem(element, value)
        return element

    def create_parent(self, document):
        """Create the parent element from ``parent_xpath`` in ``document``.

        Create the parent element to which the element representing this
        property's value must be appended.

        """
        def inner_create_element(parent, path):
            """Inner function creating the whole tree leading to the element."""
            parts = path.strip("/").split("/")
            next_tag = parts[0]
            if not len(next_tag.strip()):
                return parent
            node = parent.xpath(next_tag)
            if node:
                node = node[0]
            else:
                node = etree.Element(next_tag)
                parent.append(node)
            rest = "/".join(parts[1:])
            return inner_create_element(node, rest)

        return inner_create_element(document.getroot(), self.parent_xpath)


class XML(Decorator):
    """Access point designed to store values in an XML document."""
    ItemDecorator = XMLItem

    def __init__(self, wrapped_ap, decorated_properties, stream_property,
                 root_element):
        super(XML, self).__init__(wrapped_ap, {})
        self.stream_property = stream_property
        self.root_element = root_element
        self.decorated_properties = dict(decorated_properties)
        self.ordered_decorated_properties = decorated_properties
        for key, prop in self.decorated_properties.items():
            self.register(key, prop)

    def update_xml_tree(self, item):
        """Update the generated XML from the item unsaved values."""
        for key, prop in self.ordered_decorated_properties:
            if key in item.unsaved_properties:
                value = item.unsaved_properties.get(key)
                prop = self.decorated_properties[key]
                if prop.parent_xpath == "//":
                    parent_nodes = (item.xml_tree.getroot(),)
                else:
                    parent_nodes = item.xml_tree.xpath(prop.parent_xpath)
                if len(parent_nodes) == 0:
                    parent_node = prop.create_parent(item.xml_tree)
                elif len(parent_nodes) > 1:
                    raise ValueError("The xpath is ambiguous")
                else:
                    parent_node = parent_nodes[0]
                for child in parent_node:
                    if child.tag == prop.tag_name:
                        parent_node.remove(child)
                if prop.type == iter:
                    for atom in value:
                        parent_node.append(prop.to_xml(atom))
                else:
                    parent_node.append(prop.to_xml(value))

    def preprocess_save(self, item):
        """Function called before ``item`` is saved."""
        if len(item.unsaved_properties):
            self.update_xml_tree(item)
            stream = StringIO()
            stream.write(etree.tostring(item.xml_tree))
            item[self.stream_property] = stream
