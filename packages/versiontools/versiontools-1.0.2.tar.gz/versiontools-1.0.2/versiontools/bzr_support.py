#!/usr/bin/env python
#
# Copyright (C) 2010 Linaro Limited
#
# Author: Zygmunt Krynicki <zygmunt.krynicki@linaro.org>
#
# This file is part of versiontools.
#
# versiontools is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation
#
# versiontools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with versiontools.  If not, see <http://www.gnu.org/licenses/>.

"""
Bazaar support for versiontools
"""

import bzrlib
import bzrlib.errors
import bzrlib.branch


class BzrIntegration(object):
    """
    Bazaar integration for versiontools
    """
    def __init__(self, branch):
        self._revno = branch.last_revision_info()[0]

    @property
    def revno(self):
        """
        Revision number of the branch
        """
        return self._revno

    @classmethod
    def from_source_tree(cls, source_tree):
        """
        Initialize BzrIntegration by pointing at the source tree.
        Any file or directory inside the source tree may be used.
        """
        branch = None
        try:
            if bzrlib.__version__ >= (2, 2, 1):
                with bzrlib.initialize():
                    branch = bzrlib.branch.Branch.open_containing(source_tree)[0]
            else:
                branch = bzrlib.branch.Branch.open_containing(source_tree)[0]
        except bzrlib.errors.NotBranchError:
            import logging
            logging.warning("Unable to get branch revision because"
                            " directory %r is not a bzr branch",
                            source_tree)
        if branch:
            return cls(branch)
