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


import cherrypy

from rnaspace.ui.utils.common import common
from rnaspace.ui.utils.common import AUTH_ERROR
from rnaspace.ui.controller.error_controller import error_controller
from rnaspace.ui.model.explore.sequence_visualisation_model import sequence_visualisation_model

class sequence_visualisation_controller(object):
    """ Class sequence_visualisation_controller: the controller of the sequence view
    """

    def __init__(self):
        """ Build a sequence_visualisation_controller object defined by    
            view(type:cherrypy.Template)    the sequence view     
        """
        self.model = sequence_visualisation_model()
        
    def __fill_template(self, user_id, project_id, params, view):
        """ Fill the sequence_visualisation view by searching information into its model 
            **params(type:{})    the dictionary of all the parameters given by the user
        """
        sequence_id = self.model.get_sequence_id(params)
        view.sequence = self.model.get_sequence(user_id, project_id, sequence_id)
        view.sequence_size_to_display = self.model.sequence_size_to_display
        view.sequence_header = self.model.get_sequence_header(user_id, project_id, sequence_id)
        
    @cherrypy.expose
    def index(self, **params):
        view = common.get_template('explore/sequence_visualisation_view.tmpl')
        """ index page of split_into_2families
            **params(type:{})    the dictionary of all the parameters given by the user
        """
        if params.has_key("authkey"):
            [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
            if user_id is None or project_id is None:
                return self.error(AUTH_ERROR)
            # If the user has data on the disk
            if self.model.user_has_data(user_id):
                try:
                    self.__fill_template(user_id, project_id, params, view)
                    return view.respond()
                except:
                    return "Something wrong happened when attempting to access the specified sequence!"
            else:
                return "You're data have been deleted. For server maintenance, data are cleared after a while."
        else:
            return "You're not authorized to access this page."

    @cherrypy.expose
    def error(self, msg, authkey=None):
        error_page = error_controller()
        return error_page.get_page(msg, authkey)
