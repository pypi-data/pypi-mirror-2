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

class sequence_visualisation_model(object):
    """ Class sequence_visualisation_model: the model of the sequence view
    """
    
    sequence_size_to_display = 80
    
    def __init__(self):
        """ Build a sequence_visualisation_model object defined by    
            data_manager(type:core.data_manager)   the application data manager  
        """
        self.data_manager = data_manager()
        
    def user_has_data(self, user_id):
        """ Return True if the user has data, false else 
            user_id(type:string)   the user id
        """
        return self.data_manager.user_has_data(user_id)
    
    def get_sequence_header(self, user_id, project_id, sequence_id):
        """ Return the sequence header to display
            user_id(type:string)      the user id
            project_id(type:string)   project id the user is working on
            sequence_id(type:string)  the id of the sequence to return
        """
        return self.data_manager.get_sequence_header(user_id, project_id, sequence_id)
        
    def get_sequence(self, user_id, project_id, sequence_id):
        """ Return the sequence to display
            user_id(type:string)      the user id
            project_id(type:string)   project id the user is working on
            sequence_id(type:string)  the id of the sequence to return
        """
        return self.data_manager.get_sequence(user_id, sequence_id, project_id)
 
    def get_ids_from_authkey(self, id):
        """
        id(sting)      the id containing the user_id and the project_id
        return [user_id, project_id]
        """
        return self.data_manager.get_ids_from_authkey(id)
 
    def get_project_id(self, params):
        """ Return the current project_id
            params(type:{})     the dictionary of parameters
        """
        if params.has_key("project_id"):
            return params["project_id"]
        else:
            return None

    def get_sequence_id(self, params):
        """ Return the sequence id to return
            params(type:{})   the dictionary of parameters
        """
        if params.has_key("sequence_id"):
            return params["sequence_id"]
        else:
            return None


    def get_mount_point(self):
        return self.data_manager.get_mount_point()
