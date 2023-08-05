# tranchitella.recipe.nose
# Copyright (C) 2008-2010 Tranchitella Kft. <http://tranchtella.eu>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

from zc.buildout.easy_install import scripts
from zc.recipe.egg.egg import Eggs


class Recipe(object):
    """Buildout recipe: tranchitella.recipe.wsgi:default"""

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.options['eggs'] += '\nnose\ncoverage'
        self.script_name = options.get('script-name', self.name)

    def install(self):
        options = self.options
        egg = Eggs(self.buildout, options["recipe"], options)
        requirements, ws = egg.working_set()
        path = [pkg.location for pkg in ws]
        extra_paths = options.get('extra-paths', '')
        extra_paths = extra_paths.split()
        path.extend(extra_paths)
        defaults = options.get('defaults', '').strip()
        if defaults:
            defaults = ['nose'] + defaults.split()
            defaults = "argv=%r + sys.argv[1:]" % defaults
        scripts(
            [(self.script_name, 'nose', 'main')],
            ws, options['executable'],
            self.buildout['buildout']['bin-directory'],
            extra_paths=path,
            arguments=defaults,
        )
        return options.created()

    def update(self):
        self.install()
