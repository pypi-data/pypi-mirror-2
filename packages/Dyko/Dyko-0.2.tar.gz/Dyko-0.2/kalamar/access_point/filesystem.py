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
Filesystem
==========

Access point storing items in a filesystem.

"""

import os
import re
import io

from . import AccessPoint
from ..item import Item
from ..value import to_unicode
from ..property import Property

try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

# Redifining Python 3.x renamed functions
# pylint: disable=C0103
# pylint: disable=W0622
if "xrange" not in __builtins__:
    xrange = range
# pylint: enable=C0103
# pylint: enable=W0622

# io.IOBase has no __init__ method
# pylint: disable=W0231

class Stream(io.IOBase):
    """Fake stream opening files on demand."""
    def __init__(self, name):
        self.name = name

    def read(self):
        """Read the whole content of the file as bytes."""
        return open(self.name, "rb").read()

    def write(self, bytestring):
        """Write ``bytestring`` into the file."""
        open(self.name, "wb").write(bytestring)

# pylint: enable=W0231


class PropertyPart(object):
    """Regexp/properties couple for path parts."""
    def __init__(self, regexp, properties):
        self.regexp = regexp
        self.properties = properties

    def item_template(self, item):
        """Transform the regexp to an unicode string.

        The template string uses the python formatting syntax according to
        properties formatters. Then, the values are taken from the given
        ``item``.

        """
        parts = [part.split(")")[-1] for part
                 in self.regexp.pattern.strip("^$").split("(")]
        template = parts.pop(0)
        for part, prop in zip(parts, self.properties):
            template += prop.formatter
            template += part.replace("\\", "")
        values = []
        for prop in self.properties:
            value = item[prop.name]
            if prop.type != Item or value is None:
                values.append(value)
            else:
                values.append(value.reference_repr())
        return template % tuple(values)


class FileSystemProperty(Property):
    """Property for a FileSystem access point."""
    def __init__(self, property_type, formatter="%s", **kwargs):
        super(FileSystemProperty, self).__init__(property_type, **kwargs)
        self.formatter = formatter


class FileSystemItem(Item):
    """Item stored as a file."""
    @property
    def filename(self):
        """Absolute path of the item."""
        return self.access_point._item_filename(self)

    @property
    def relative_filename(self):
        """Relative path of the item, from the access point root."""
        return self.access_point._item_filename(self, "")


class FileSystem(AccessPoint):
    """Store each item in a file."""
    ItemClass = FileSystemItem

    def __init__(self, root_dir, pattern, properties,
                 content_property="content"):
        self.root_dir = root_dir
        self.content_property = content_property

        self._ordered_properties = tuple(
            (prop, FileSystemProperty(unicode)) if isinstance(prop, basestring)
            else prop # Assume a (name, Property_instance) tuple.
            for prop in properties)

        properties = dict(self._ordered_properties)
        properties[content_property] = FileSystemProperty(io.IOBase)
        # All properties here are in the identity
        identity_properties = tuple(
            name for name, prop in self._ordered_properties
            if prop.relation != "one-to-many")
        super(FileSystem, self).__init__(properties, identity_properties)

        pattern_parts = pattern.split("/")
        props_iter = iter(self.identity_properties)
        self.properties_per_path_part = []
        for part in pattern_parts:
            regexp = re.compile("^%s$" % part)
            props = tuple(next(props_iter) for i in xrange(regexp.groups))
            self.properties_per_path_part.append(PropertyPart(regexp, props))

    def _item_filename(self, item, root=None):
        """Item filename."""
        root = self.root_dir if root is None else root
        return os.path.join(root, *(
                property_part.item_template(item)
                for property_part in self.properties_per_path_part))

    def search(self, request):
        def walk(root, remaining_path_parts, previous_properties=()):
            """Walk through filesystem from ``root`` yielding matching items."""
            property_part = remaining_path_parts[0]
            remaining_path_parts = remaining_path_parts[1:]
            for basename in os.listdir(root):
                match = property_part.regexp.match(basename)
                if not match:
                    continue
                values = match.groups()
                properties = dict(zip(property_part.properties, values ))
                properties.update(previous_properties)
                path = os.path.join(root, basename)
                if remaining_path_parts and os.path.isdir(path):
                    for item in walk(path, remaining_path_parts, properties):
                        yield item
                if not remaining_path_parts and not os.path.isdir(path):
                    def defered_open():
                        """Opener for ``item``."""
                        return lambda item: (Stream(item.filename),)
                    lazy_loaders = {self.content_property : defered_open()}
                    item_properties = {}
                    for prop, value in properties.items():
                        if value == "None":
                            value = None
                        if prop.relation is None:
                            item_properties[prop.name] = value
                        elif prop.relation == "many-to-one":
                            lazy_loaders[prop.name] = \
                                prop.remote_ap.loader_from_reference_repr(value)
                        else:
                            lazy_loaders[prop.name] = \
                                self._default_loader({}, prop)
                    item_properties = dict(
                        (prop.name, to_unicode(value)) for prop, value
                        in properties.items() if prop.relation is None)
                    item = self.create(item_properties, lazy_loaders)
                    item.saved = True
                    if request.test(item):
                        yield item

        return walk(self.root_dir, self.properties_per_path_part)

    def delete(self, item):
        filename = self._item_filename(item)
        os.remove(filename)
        basedir = os.path.dirname(filename)
        if not os.listdir(basedir):
            os.removedirs(basedir)

    def create(self, properties=None, lazy_loaders=None):
        properties = properties or {}
        lazy_loaders = lazy_loaders or {}
        if self.content_property not in properties \
                and self.content_property not in lazy_loaders:
            properties[self.content_property] = StringIO()
        return super(FileSystem, self).create(properties, lazy_loaders)

    def save(self, item):
        content = item[self.content_property]
        try:
            content.seek(0)
        except: # pragma: no cover
            # No real way found to know if we can't seek, it sometimes happen
            pass
        filename = self._item_filename(item)
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with Stream(filename) as file_descriptor:
            file_descriptor.write(content.read())
        item.saved = True
