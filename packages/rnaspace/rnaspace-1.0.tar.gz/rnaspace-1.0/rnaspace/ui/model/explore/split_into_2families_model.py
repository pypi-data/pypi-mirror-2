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


import cgi

from rnaspace.core.data_manager import data_manager
from rnaspace.core.trace.event import edit_rna_event
from rnaspace.core.trace.event import disk_error_event
from rnaspace.core.exceptions import disk_error


class split_into_2families_model(object):
    """ Class split_into_2families_model: the model of the split_into_2families popup
    """
    
    def __init__(self):
        """ Build a split_into_2families_model object defined by    
            data_manager(type:core.data_manager)   the application data manager  
        """
        self.data_manager = data_manager()
        
    def user_has_data(self, user_id):
        """ Return True if the user has data, false else 
            user_id(type:string)   the user id
        """
        return self.data_manager.user_has_data(user_id)
    
    def get_putative_rnas(self, user_id, project_id, params):
        """ Return a dictionary of putative_rna indexed by their sys_id
            user_id(type:string)      the user id
            project_id(type:string)   project id the user is working on
            params(type:{})         the dictionary of all the parameters
        """
        result_table = []
        if params.has_key("nb_putative_rnas"):
            rnas = self.data_manager.get_putative_rnas(user_id, project_id)
            for i in range(int(params["nb_putative_rnas"])):
                param_name = "putative_rna" + str(i)
                for rna in rnas:    
                    if rna.sys_id == params[param_name]:
                        result_table.append(rna)
        return result_table
                
    def get_params(self, params):
        """ Return a dictionary of parameters
            params(type:{})   the dictionary of parameters to format
        """
        try:
            p = cgi.parse_qs(params["data"])
            for key, val in p.items():
                if len(val) == 1:
                    p[key] = val[0]
            p["family1_name"] = params["family1_name"]
            p["family2_name"] = params["family2_name"]
            return p
        except:
            return params   

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

    def update_putative_rnas(self, user_id, project_id, params):
        """ Update the family field of the putative_rnas specified
            user_id(type:string)      user id of the connected user
            project_id(type:string)   project id the user is working on
            params(type:{})         the dictionary of parameters
        """
        family_1 = self.__get_family(1, params)
        family_2 = self.__get_family(2, params)

        if (family_1 != ""):
            rnas_id_1 = []
            for i in range(self.__get_nb_putative_rnas_in_family(1, params)):
                id = "to_family_1_" + str(i)
                rnas_id_1.append(params[id])
                
            try:
                self.data_manager.update_putative_rnas_family(user_id,
                                                              project_id,
                                                              rnas_id_1,
                                                              family_1)
            except disk_error, e:
                mail = self.data_manager.get_user_email(user_id, project_id)
                project_size = self.data_manager.get_project_used_space(user_id,
                                                                    project_id)
                ev = disk_error_event(user_id, project_id, mail, e.message,
                                      project_size)
            
                self.data_manager.update_project_trace(user_id, project_id,
                                                       [ev])
                raise

            events = []
            for r in rnas_id_1:
                events.append( edit_rna_event(user_id, project_id,
                                              self.data_manager.get_user_email(user_id,project_id),
                                              r,
                                              family = family_1 ) )
            self.data_manager.update_project_trace(user_id,project_id, events)

        
        if (family_2 != ""):
            rnas_id_2 = []
            for i in range(self.__get_nb_putative_rnas_in_family(2, params)):
                id = "to_family_2_" + str(i)
                rnas_id_2.append(params[id])
                
            try:
                self.data_manager.update_putative_rnas_family(user_id,
                                                              project_id,
                                                              rnas_id_2,
                                                              family_2)
            except disk_error, e:
                mail = self.data_manager.get_user_email(user_id, project_id)
                project_size = self.data_manager.get_project_used_space(user_id,
                                                                    project_id)
                ev = disk_error_event(user_id, project_id, mail, e.message,
                                      project_size)
            
                self.data_manager.update_project_trace(user_id, project_id,
                                                       [ev])
                raise

            events = []
            for r in rnas_id_2:
                events.append( edit_rna_event(user_id, project_id,
                                              self.data_manager.get_user_email(user_id,project_id),
                                              r,
                                              family = family_2 ) )
            self.data_manager.update_project_trace(user_id,project_id, events)

    def get_action(self, params):
        """ Return the action
            params(type:{})     the dictionary of parameters
        """
        if params.has_key("action"):
            return params["action"]
        else:
            return None 

    def __get_family(self, family, params):
        """ Return the family name defined by its family number
            family(type:integer)  the family number
            params(type:{})     the dictionary of parameters
        """
        family_name = "family" + str(family) + "_name"
        if params.has_key(family_name):
            return params[family_name]
        else:
            return ""

    def __get_nb_putative_rnas_in_family(self, family, params):
        """ Return the number of putative_rna in the family defined by its number
            family(type:integer)  the family number
            params(type:{})   the dictionary of parameters
        """
        nb_in_family = "nb_family" + str(family)
        if params.has_key(nb_in_family):
            return int(params[nb_in_family])
        else:
            return 0

    def get_mount_point(self):
        return self.data_manager.get_mount_point()


