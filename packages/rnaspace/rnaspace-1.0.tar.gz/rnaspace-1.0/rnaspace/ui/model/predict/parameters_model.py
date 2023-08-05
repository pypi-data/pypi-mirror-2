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


from rnaspace.core.prediction.software_manager import software_manager
from rnaspace.core.data_manager import data_manager

class parameters_model:

    def __init__(self):
        self.sm = software_manager()
        self.data_m = data_manager()

    def get_software(self, softname, softtype):        
        return self.sm.get_software(softname, softtype.split('_')[0])
        
    def check_param(self, softname, softtype, params):
        """
        check if the parameters are ok for the corresponding software

        Return(string)  None if evrything ok, an an error message if not

        params({}):     a dictionnary containing all parameters and their values
        """
        return self.sm.check_parameters(softname, softtype, params)

    def get_opts(self, params):
        """
        extract options in the form parameters

        Return({})    dictionary containing options and their values

        params({})    dictionary containaing the form parameters
        """
        p = {}
        for key in params:
            if key.startswith('select'):
                p['_'.join(i for i in key.split('_')[1:])] = "True"
            elif key.endswith('option'):
                right_key = '_'.join( opt for opt in key.split('_')[:-3])
                p[right_key] = params[key]
                    
        if len(p) == 0:
            p = None

        return p        

    def has_user_done_a_run(self, user_id, project_id):
        """
        Return                True if the user has done a run yet,
                              False otherwise
        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        """
        try:
            return self.data_m.user_has_done_a_run(user_id, project_id)
        except:
            return False


    def get_ids_from_authkey(self, id):
        """
        id(sting)      the id containing the user_id and the project_id
        return [user_id, project_id]
        """
        return self.data_m.get_ids_from_authkey(id)

    def get_authkey(self, user_id, project_id):
        """
        user_id(sting)      the user_id
        project_id(string)  the project_id
        return the id
        """
        return self.data_m.get_authkey(user_id, project_id)

    def is_an_authentification_platform(self):
        return self.data_m.is_an_authentification_platform()

    def get_mount_point(self):
        return self.data_m.get_mount_point()
