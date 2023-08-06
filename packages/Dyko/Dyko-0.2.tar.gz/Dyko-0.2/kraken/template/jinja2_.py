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
# along with Koral library.  If not, see <http://www.gnu.org/licenses/>.

"""
Jinja2
======

`Jinja2 <http://jinja.pocoo.org/2/>`_ engine support for Koral.

"""

from . import BaseEngine


class Jinja2Engine(BaseEngine):
    """Koral engine for Jinja2."""
    name = "jinja2"
    
    def __init__(self, *args, **kwargs):
        super(Jinja2Engine, self).__init__(*args, **kwargs)
        from jinja2 import Environment, FileSystemLoader
        self._env = Environment(loader=FileSystemLoader(self.path_to_root))
        
    def render(self, template_name, values, lang, modifiers):
        template = self._env.get_template(template_name)
        return template.render(**values)
