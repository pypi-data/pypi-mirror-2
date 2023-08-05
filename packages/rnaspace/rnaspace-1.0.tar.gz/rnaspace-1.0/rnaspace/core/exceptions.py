#
# RNAspace: non-coding RNA annotation platform
# Copyright (C) 2009  CNRS, INRA, INRIA, Univ. Paris-Sud 11
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


class disk_error(Exception):
    """
    Exception to be raised when no space is available to perform
    an operation
    """

    prna_message = "some predictions have not been saved"
    alignment_message = "some alignments have not been saved"
    sequence_message = "some sequences have not been saved"

    def __init__(self, user_id, project_id, message=None):
        self.user_id = user_id
        self.project_id = project_id
        if message is not None:
            self.message = message
        else:
            self.message = "Sorry, no more space available."

    def __str__(self):
        return self.message
    

class project_space_error(disk_error):
    """
    Exception to be raised when no space available for a specified project
    """

    def __init__(self, user_id, project_id, message=None):
        disk_error.__init__(self, user_id, project_id, message)

    def __str__(self):
        text = "No more space available for project %s, "%self.project_id
        return text + self.message


class user_space_error(disk_error):
    """
    Exception to be raised when no space available for a specified user
    """

    def __init__(self, user_id, project_id, message=None):
        disk_error.__init__(self, user_id, project_id, message)
        
    def __str__(self):
        text = "No more space available for user %s, "%self.user_id
        return text + self.message
