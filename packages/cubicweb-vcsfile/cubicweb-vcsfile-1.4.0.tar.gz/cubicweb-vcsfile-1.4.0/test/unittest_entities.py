from utils import VCSFileTC
from logilab.common.decorators import clear_cache

class BranchHeadsTC(VCSFileTC):
    repo_path = u'testrepohg_branches'
    repo_type = u'mercurial'

    def rev(self, file, *args):
        return self.vcsrepo.versioned_file('', file).branch_head(*args).revision

    def test_vcsrm(self):
        # XXX outcome depends on method names (=> execution order)
        vf = self.vcsrepo.versioned_file('', 'README')
        vf.vcs_rm()
        self.commit()
        clear_cache(vf, 'branch_head')
        clear_cache(vf, 'version_content')
        self.assertTrue(vf.deleted_in_branch())
        self.assertTrue(vf.head.rev.parent_revision)
        self.assertEquals(len(vf.head.rev.reverse_at_revision), 3,
                          vf.head.rev.reverse_at_revision)

    def test_branch_head_no_arg(self):
        self.assertEquals(self.rev('README'), 1)
        self.assertEquals(self.rev('file.txt'), 4)
        self.assertEquals(self.rev('otherfile.txt'), 4)

    def test_branch_head_default(self):
        self.assertEquals(self.rev('README', 'default'), 1)
        self.assertEquals(self.rev('file.txt', 'default'), 4)
        self.assertEquals(self.rev('otherfile.txt', 'default'), 4)

    def test_branch_head_branch1(self):
        self.assertEquals(self.rev('README', 'branch1'), 1)
        self.assertEquals(self.rev('file.txt', 'branch1'), 2)
        self.assertEquals(self.rev('otherfile.txt', 'branch1'), 3)


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
