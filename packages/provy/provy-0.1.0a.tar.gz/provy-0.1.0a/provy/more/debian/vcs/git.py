#!/usr/bin/python
# -*- coding: utf-8 -*-

from provy.core import Role
from provy.more.debian.package.aptitude import AptitudeRole

class GitRole(Role):
    def provision(self):
        with self.using(AptitudeRole) as role:
            role.ensure_up_to_date()
            role.ensure_package_installed('git-core')

    def ensure_repository(self, repo, path, owner=None, branch=None):
        if not self.remote_exists_dir(path):
            self.log("Repository for %s does not exist! Cloning..." % repo)
            self.execute("git clone %s %s" % (repo, path), sudo=True, stdout=False)
            self.log("Repository %s cloned!" % repo)

        branch_name = "# On branch %s" % branch
        if branch and not branch_name in self.execute("git --git-dir=\"%s/.git\" --work-tree=\"%s\" status" % (path, path), 
                sudo=True, stdout=False):
            self.log("Repository for %s is not in branch %s ! Switching..." % (repo, branch))
            self.execute("git --git-dir=\"%s/.git\" --work-tree=\"%s\" checkout %s" % (path, path, branch))
            self.log("Repository %s currently in branch %s!" % (repo, branch))

        if owner:
            self.change_dir_owner(path, owner)
