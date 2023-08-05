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


import time

from rnaspace.ui.utils.common import common
from rnaspace.ui.model.infobar_model import infobar_model

class infobar_controller(object):
    """ Class infobar_controller: the controller of the infobar
    """
    
    def __init__(self):
        """ Build an infobar_controller object defined by    
            view(type:cherrypy.Template)      the error page view    
        """    
        self.model = infobar_model()
        self.view = common.get_template('infobar_view.tmpl')
        self.soft_view = common.get_template('infobar_soft_view.tmpl')
    
    def __fill_template(self, user_id, project_id):
        mount_point = self.model.get_mount_point()
        self.view.mount_point = mount_point
        self.view.user_id = user_id
        self.view.projects = self.model.get_user_projects(user_id, project_id)
        self.view.nb_sequences = self.model.get_nb_sequences(user_id, project_id)
        self.view.nb_predictions = self.model.get_nb_predictions(user_id, project_id)
        self.view.nb_alignments = self.model.get_nb_alignments(user_id, project_id)
        self.view.project_used_space = self.model.get_project_used_space(user_id, project_id)
        self.view.unknown_user = self.model.get_unknown_user_name()

        history = self.model.get_history(user_id, project_id)
        if history is not None:
            sorted_dates = history.keys()
            sorted_dates.sort(reverse=True)
            dates = {}
            for date in sorted_dates:
                time_value = date.split("-")
                now = str(time.localtime()[1]) + "/" + str(time.localtime()[2]) + "/" + str(time.localtime()[0])
                if time_value[0] == now:
                    h = time_value[1].split(":")
                    h = h[0] + ":" + h[1]
                    dates[date] = h
                else: 
                    dates[date] = time_value[0]   
            self.view.sorted_dates = sorted_dates
            self.view.history = history
            self.view.dates = dates
        else:
            self.view.sorted_dates = None
            self.view.dates = None
            self.view.history = None
        self.view.history_size = self.model.history_size
        
        if user_id != self.model.get_unknown_user_name():
            self.view.user_used_space = self.model.get_user_used_space(user_id) 
            self.view.available_space = self.model.get_available_space()

    def get_infobar(self, user_id, project_id):
        self.__fill_template(user_id, project_id)
        return self.view.respond()
