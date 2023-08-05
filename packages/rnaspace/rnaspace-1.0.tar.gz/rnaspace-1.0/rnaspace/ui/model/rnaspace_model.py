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


from rnaspace.core.data_manager import data_manager

class rnaspace_model(object):
    """ Class rnaspace_model: the model of the home page
    """

    def __init__(self):
        """ Build an infobar_model object defined by    
            data_manager(type:core.data_manager)   the application data manager  
        """
        self.data_manager = data_manager()
        
        
    def is_user_active(self, user_id, project_id):
        """
        Return                True if the user has done something yet, False otherwise
        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        """
        try:
            ids = self.data_manager.get_sequences_id(user_id, project_id)
            return len(ids) != 0
        except:
            return False
        
    def has_user_done_a_run(self, user_id, project_id):
        """
        Return                True if the user has done a run yet, False otherwise
        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        """
        try:
            return self.data_manager.user_has_done_a_run(user_id, project_id)
        except:
            return False

    def get_ids_from_authkey(self, id):
        """
        id(sting)      the id containing the user_id and the project_id
        return [user_id, project_id]
        """
        return self.data_manager.get_ids_from_authkey(id)

    def get_authkey(self, user_id, project_id):
        """
        user_id(sting)      the user_id
        project_id(string)  the project_id
        return the id
        """
        return self.data_manager.get_authkey(user_id, project_id)

    def is_an_authentification_platform(self):
        return self.data_manager.is_an_authentification_platform()
    
    def get_mount_point(self):
        return self.data_manager.get_mount_point()
