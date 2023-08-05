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

from bzrlib.plugins.colo.tests.script import ScriptTestCase


class TestColoSyncFrom(ScriptTestCase):

    def test_sync(self):
        self.run_script("""
$ bzr colo-init remote
$ bzr colo-init local
$ cd local
$ bzr colo-sync-from ../remote
2>Updating branch trunk from colo:../remote:trunk.
No revisions to pull.
""")

    def test_sync_nontrivial(self):
        self.run_script("""
$ bzr colo-init remote
$ bzr colo-init local
$ cd remote
$ echo content > file
$ bzr add
$ bzr ci -m 'a revision'
$ cd ../local
$ bzr colo-sync-from ../remote
2>Updating branch trunk from colo:../remote:trunk.
2>All changes applied successfully.
Now on revision 1.
""")

    def test_sync_missing_branch(self):
        self.run_script("""
$ bzr colo-init remote
$ bzr colo-init local
$ cd local
$ bzr colo-branch other
$ bzr colo-sync-from ../remote
$ bzr colo-branches
* other
  trunk
""")

    def test_sync_creates_branch(self):
        self.run_script("""
$ bzr colo-init remote
$ bzr colo-init local
$ cd remote
$ bzr colo-branch other
$ cd ../local
$ bzr colo-sync-from ../remote
$ bzr colo-branches
  other
* trunk
""")


    def test_sync_diverged(self):
        self.run_script("""
$ bzr colo-init remote
$ bzr colo-init local
$ cd remote
$ echo content > file
$ bzr add
$ bzr ci -m 'a revision in remote branch'
$ cd ../local
$ echo stuff > file1
$ bzr add
$ bzr ci -m 'a different revision in local branch'
""")
        self.run_bzr_error(['These branches have diverged'],
                           ['colo-sync-from', '../remote'])

    def test_sync_multiple_diverged(self):
        self.run_script("""
$ bzr colo-init local
$ bzr colo-init remote
$ cd remote
$ echo content > file
$ bzr add
$ bzr ci -m 'trunk revision'
$ bzr colo-branch other
$ cd ../local
$ echo stuff > file
$ bzr add
$ bzr ci -m 'a different trunk revision'
$ bzr colo-sync-from ../remote
2>Creating new branch other from colo:../remote:other.
2>Branched 1 revision(s).
2>Updating branch trunk from colo:../remote:trunk.
2>bzr: ERROR: These branches have diverged...
""")

    def test_sync_overwrite(self):
        self.run_script("""
$ bzr colo-init remote
$ bzr colo-init local
$ cd remote
$ echo content > file
$ bzr add
$ bzr ci -m 'a revision in remote branch'
$ cd ../local
$ echo stuff > file1
$ bzr add
$ bzr ci -m 'a different revision in local branch'
$ bzr colo-sync-from --overwrite ../remote
2>Updating branch trunk from colo:../remote:trunk.
2>All changes applied successfully.
Now on revision 1.
""")

    def test_sync_from_empty(self):
        self.run_script("""
$ mkdir empty
$ bzr colo-init local
$ cd local
$ bzr colo-sync-from ../empty
2>bzr: ERROR: No colocated workspace in ../empty
""")

    def test_sync_from_standalone(self):
        self.run_script("""
$ bzr colo-init local
$ bzr init standalone
$ cd local
$ bzr colo-sync-to ../standalone
2>bzr: ERROR: No colocated workspace in ../standalone
""")


class TestColoSyncTo(ScriptTestCase):

    def test_sync(self):
        self.run_script("""
$ bzr colo-init remote
$ bzr colo-init local
$ cd local
$ bzr colo-sync-to ../remote
2>Updating colo:../remote:trunk from trunk.
2>No new revisions to push.
""")

    def test_sync_nontrivial(self):
        self.run_script("""
$ bzr colo-init remote
$ bzr colo-init local
$ cd local
$ echo content > file
$ bzr add
$ bzr ci -m 'first revision'
$ bzr colo-sync-to ../remote
2>Updating colo:../remote:trunk from trunk.
2>Pushed up to revision 1.
$ cd ../remote
$ bzr revno
1
""")

    def test_sync_to_empty(self):
        self.run_script("""
$ mkdir branch
$ bzr colo-init workspace
$ cd workspace
$ bzr colo-sync-to ../branch
2>bzr: ERROR: No colocated workspace in .../branch
""")

    def test_sync_to_standalone(self):
        self.run_script("""
$ bzr colo-init local
$ bzr init standalone
$ cd local
$ bzr colo-sync-to ../standalone
2>bzr: ERROR: No colocated workspace in ../standalone
""")

    def test_sync_to_no_trees(self):
        self.run_script("""
$ bzr colo-init --no-tree remote
$ bzr colo-init local
$ cd local
$ bzr colo-sync-to ../remote
2>Updating colo:../remote:trunk from trunk.
2>No new revisions to push.
$ cd ../remote
$ bzr colo-branches
  trunk
""")

    def test_sync_to_creates_branch(self):
        self.run_script("""
$ bzr colo-init remote
$ bzr colo-init local
$ cd local
$ bzr colo-branch other
$ bzr colo-sync-to ../remote
2>Updating colo:../remote:other from other.
2>Created new branch.
2>Updating colo:../remote:trunk from trunk.
2>No new revisions to push.
$ cd ../remote
$ bzr colo-branches
  other
* trunk
""")

    def test_sync_to_diverged(self):
        self.run_script("""
$ bzr colo-init remote
$ bzr colo-init local
$ cd remote
$ echo content > file
$ bzr add
$ bzr ci -m 'a revision'
$ cd ../local
$ echo stuff > file
$ bzr add
$ bzr ci -m 'a separate revision'
$ bzr colo-sync-to ../remote
2>Updating colo:../remote:trunk from trunk.
2>bzr: ERROR: These branches have diverged. ...
""")
