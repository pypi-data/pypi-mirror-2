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
from rnaspace.ui.model.explore.split_into_2families_model import split_into_2families_model
from rnaspace.core.exceptions import disk_error

DISK_ERROR =\
"""
<br />
Sorry, no more space available. <br />
You can not modify predictions.
<br /><br />
Return to <a href="%s">Explore page</a>.
"""


class split_into_2families_controller(object):
    """ Class split_into_2families_controller: the controller of the split into 2 families popup
    """  

    def __init__(self):
        """ Build a split_into_2families_controller object defined by    
            view(type:cherrypy.Template)                     the split_into_2families view    
            model(type:ui.model.split_into_2families_model)  the split_into_2families model   
        """
        self.view = common.get_template('explore/split_into_2families_view.tmpl')
        self.model = split_into_2families_model()
    
    def __fill_template(self, user_id, project_id, params):
        """ Fill the split_into_2families view by searching information into its model 
            params(type:{})    the dictionary of all the parameters given by the user
        """
        mount_point = self.model.get_mount_point()
        self.view.authkey = self.model.get_authkey(user_id, project_id)
        self.view.putative_rnas = self.model.get_putative_rnas(user_id, project_id, params)
        self.view.mount_point = mount_point
    @cherrypy.expose
    def index(self, **params):
        """ index page of split_into_2families
            **params(type:{})    the dictionary of all the parameters given by the user
        """
        if params.has_key("authkey"):
            [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
            if user_id is None or project_id is None:
                return self.error(AUTH_ERROR)
            # If the user has data on the disk
            if self.model.user_has_data(user_id): 
                if self.model.get_action(params) == "split_into_2_families":
                    
                    r_params = self.model.get_params(params)
                    try:
                        self.model.update_putative_rnas(user_id, project_id,
                                                        r_params)
                    except disk_error, error:
                        mount_point = self.model.get_mount_point()
                        authkey = self.model.get_authkey(user_id, project_id)
                        url = mount_point + "explore/index?authkey=" + authkey
                        message = DISK_ERROR%url
                        return self.error(message, authkey)
                    return ""
                else:
                    self.__fill_template(user_id, project_id, params)
                return self.view.respond()
            else:
                return "You're data have been deleted. For server maintenance, data are cleared after a while."
        else:
            return "You're not authorized to access this page."
        
    @cherrypy.expose
    def error(self, msg, authkey=None):
        error_page = error_controller()
        return error_page.get_page(msg, authkey)
