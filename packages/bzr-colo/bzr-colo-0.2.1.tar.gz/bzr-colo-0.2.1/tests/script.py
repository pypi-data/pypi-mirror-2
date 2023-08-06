
# Copyright 2010 Neil Martinsen-Burrell

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


import bzrlib
from bzrlib.lazy_import import lazy_import
lazy_import(globals(),'''
            from bzrlib import (errors,
                                tests,
                               )
            from bzrlib.tests import script
            ''')

class ScriptTestCase(script.TestCaseWithTransportAndScript):

    def run_script(self, script):
        if bzrlib.version_info >= (2, 3):
            super(ScriptTestCase, self).run_script(script,
                null_output_matches_anything=True)
        else:
            super(ScriptTestCase, self).run_script(script)

