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

import os
from bzrlib.tests import TestCaseWithTransport

class TestQBzrCommands(TestCaseWithTransport):

    def test_disabled(self):
        # can't disable plugins in tests, following code is from a dream

        #os.environ['BZR_DISABLE_PLUGINS']='qbzr'
        #self.run_bzr_error(['qbranches requires the qbzr plugin'],
        #                   ['qbranches'])
        pass

    def test_enabled(self):
        try:
            from bzrlib.plugins import qbzr
        except ImportError:
            return
        self.run_bzr_error(['No colocated workspace'],
                           ['qbranches'])
