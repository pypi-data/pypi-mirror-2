import re
import os.path as osp
from os import remove
from shutil import rmtree

from logilab.common.shellutils import unzip

from cubicweb.devtools.testlib import CubicWebTC

from cubes.vcsfile import bridge

HERE = osp.dirname(__file__) or '.'

for repo in ('testrepohg', 'testrepohg_branches', 'testrepohg_renaming'):
    repopath = osp.join(HERE, repo)
    if osp.exists(repopath):
        rmtree(repopath)
    unzip('%s.zip' % repo,  HERE)


def remove_eid(string):
    return re.sub('#\d+', '#EID', string)


class VCSFileTC(CubicWebTC):
    repo_path = u'testrepo'
    repo_type = u'subversion'
    repo_encoding = u'utf-8'
    repo_subpath = None

    def setUp(self, init_cw=True):
        bridge._REPOHDLRS.clear()
        if init_cw:
            CubicWebTC.setUp(self)
        self.vcsrepo = self.request().create_entity('Repository', type=self.repo_type,
                                                    path=self.repo_path,
                                                    subpath=self.repo_subpath,
                                                    encoding=self.repo_encoding)
        self.repoeid = self.vcsrepo.eid
        self.commit()
        # set commit_every to test it on the way
        from time import clock
        t = clock()
        bridge.import_content(self.repo, commitevery=3)
        #print 'import content time %.3f' % (clock() - t)
