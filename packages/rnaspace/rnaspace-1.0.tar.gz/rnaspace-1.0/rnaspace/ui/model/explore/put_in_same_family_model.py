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
from rnaspace.core.trace.event import edit_rna_event
from rnaspace.core.trace.event import disk_error_event
from rnaspace.core.exceptions import disk_error

class put_in_same_family_model(object):
    """ Class put_in_same_family_model: the model of put_in_same_familie
    """
    
    def __init__(self):
        """ Build a put_in_same_family_model object defined by    
            data_manager(type:core.data_manager)   the application data manager  
        """
        self.data_manager = data_manager()
        
    def user_has_data(self, user_id):
        """ Return True if the user has data, false else 
            user_id(type:string)   the user id
        """
        return self.data_manager.user_has_data(user_id)
    
    def get_action(self, params):
        """ Return the action
            params(type:{})     the dictionary of parameters
        """
        if params.has_key("action"):
            return params["action"]
        else:
            return None

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

    def get_putative_rnas(self, params):
        putative_rnas = []
        for rna in range(int(params["nb_putative_rnas"])):
            putative_rnas.append(params["putative_rna"+str(rna)])
        return putative_rnas
        
    def put_in_same_family(self, user_id, project_id, params):
        rnas_to_update = self.get_putative_rnas(params)
        new_family = self.__get_new_family(params)
        
        try:
            self.data_manager.update_putative_rnas_family(user_id, project_id,
                                                          rnas_to_update,
                                                          new_family)
        except disk_error, e:
            mail = self.data_manager.get_user_email(user_id, project_id)
            project_size = self.data_manager.get_project_used_space(user_id,
                                                                    project_id)
            ev = disk_error_event(user_id, project_id, mail, e.message,
                                  project_size)
            
            self.data_manager.update_project_trace(user_id, project_id, [ev])
            raise

        events = []
        for r in rnas_to_update:
             events.append( edit_rna_event(user_id, project_id,
                                           self.data_manager.get_user_email(user_id,project_id),
                                           r,
                                           family = new_family ) )
        self.data_manager.update_project_trace(user_id,project_id, events)

    def __get_new_family (self, params):
        if params.has_key("family"):
            return params["family"]
        else:
            return "" 

    def get_mount_point(self):
        return self.data_manager.get_mount_point()
