# -*- coding: iso-8859-1 -*-
#
# $Id:permissions.py 1255 2009-09-24 08:47:42Z amelung $
#
# Copyright � 2004 Otto-von-Guericke-Universit�t Magdeburg
#
# This file is part of ECQuiz.
#
# ECQuiz is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# ECQuiz is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ECQuiz; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

"""
Permissions used by ECQuiz
"""

from config import PROJECTNAME
from Products.CMFCore.permissions import setDefaultRoles, \
     ModifyPortalContent#, AddPortalContent, View

ROLE_RESULT_GRADER = 'ECQuizResultGrader'
ROLE_RESULT_VIEWER = 'ECQuizResultViewer'

PERMISSION_INTERROGATOR        = ModifyPortalContent
PERMISSION_STUDENT             = 'ECQuiz Access Contents'
PERMISSION_RESULT_READ         = 'ECQuiz Read Result'
setDefaultRoles(PERMISSION_RESULT_READ,  (ROLE_RESULT_VIEWER,))
PERMISSION_RESULT_WRITE        = 'ECQuiz Write Result'

PERMISSION_GRADE = '%s: Grade Assignments' % PROJECTNAME
setDefaultRoles(PERMISSION_GRADE,  ('Manager', ROLE_RESULT_GRADER,))

PERMISSION_ADD_MCTEST = '%s: Add Quiz' % PROJECTNAME
setDefaultRoles(PERMISSION_ADD_MCTEST, ('Manager', 'Owner',))

# PERMISSION_DEFAULT_ADD_CONTENT = AddPortalContent
# setDefaultRoles(PERMISSION_DEFAULT_ADD_CONTENT, ('Manager', 'Owner',))

ADD_CONTENT_PERMISSIONS = {
    'ECQuiz': PERMISSION_ADD_MCTEST,
}
