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


import math

from rnaspace.core.data_manager import data_manager

class infobar_model(object):
    """ Class infobar_model: the model of the infobar
    """

    history_size = 5

    def __init__(self):
        """ Build an infobar_model object defined by    
            data_manager(type:core.data_manager)   the application data manager  
        """
        self.data_manager = data_manager()
        
    def get_user_projects(self, user_id, project_id):
        """
        Return                the user projects' id
        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        """
        projects = []     
        if user_id == self.get_unknown_user_name():
            projects.append(project_id)
        #else:
        #    return self.data_manager.get_user_projects(user_id)
        return projects
    
    def get_history(self, user_id, project_id):
        try:
            return self.data_manager.get_history(user_id, project_id)
        except:
            return None
        
    def get_nb_sequences(self, user_id, project_id):
        try:
            seq_ids = self.data_manager.get_sequences_id(user_id, project_id)
            return len(seq_ids)
        except:
            return 0

    def get_nb_predictions(self, user_id, project_id):
        prnas = self.data_manager.get_putative_rnas(user_id, project_id)
        return len(prnas)

    def get_nb_alignments(self, user_id, project_id):
        return self.data_manager.get_nb_alignments(user_id, project_id)

    def get_available_space(self):
        try:
            octets_link = ["octets", "Ko", "Mo", "Go", "To", "Po", "Eo", "Zo"]
            space = self.data_manager.get_available_space()
            p = int(math.ceil(float(len(str(space)))/float(3) - float(1)))
            pow_needed = p * 10
            pow_needed = pow(2, pow_needed)
            value = str(float(space)/float(pow_needed))
            tmp = value.split(".")
            value = tmp[0] + "." + tmp[1][:2]
            try:
                value = value + " " + octets_link[p]
            except:
                value = str(space) + " octets"
            return value
        except:
            return "0 octets"
        
    def get_user_used_space(self, user_id):
        if user_id == None:
            user_id = self.get_unknown_user_name()
        try:
            octets_link = ["octets", "Ko", "Mo", "Go", "To", "Po", "Eo", "Zo"]
            space = self.data_manager.get_user_used_space(user_id)
            p = int(math.ceil(float(len(str(space)))/float(3) - float(1)))
            pow_needed = p * 10
            pow_needed = pow(2, pow_needed)
            value = str(float(space)/float(pow_needed))
            tmp = value.split(".")
            value = tmp[0] + "." + tmp[1][:2]
            try:
                value = value + " " + octets_link[p]
            except:
                value = str(space) + " octets"
            return value
        except:
            return "0 octets"

    def get_project_used_space(self, user_id, project_id):
        try:
            octets_link = ["octets", "Ko", "Mo", "Go", "To", "Po", "Eo", "Zo"]
            space = self.data_manager.get_project_size(user_id, project_id)
            p = int(math.ceil(float(len(str(space)))/float(3) - float(1)))
            pow_needed = p * 10
            pow_needed = pow(2, pow_needed)
            value = str(float(space)/float(pow_needed))
            tmp = value.split(".")
            value = tmp[0] + "." + tmp[1][:2]
            try:
                value = value + " " + octets_link[p]
            except:
                value = str(space) + " octets"
            return value
        except:
            return "0 octets"

    def get_unknown_user_name(self):
        return self.data_manager.get_unknown_user_name()
    
    def get_mount_point(self):
        return self.data_manager.get_mount_point()
