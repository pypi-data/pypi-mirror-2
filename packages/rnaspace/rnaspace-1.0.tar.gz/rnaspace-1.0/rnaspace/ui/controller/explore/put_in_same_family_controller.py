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
from rnaspace.ui.model.explore.put_in_same_family_model import put_in_same_family_model
from rnaspace.ui.controller.error_controller import error_controller
from rnaspace.core.exceptions import disk_error


DISK_ERROR =\
"""
<br />
Sorry, no more space available. <br />
You can not modify predictions.
<br /><br />
Return to <a href="%s">Explore page</a>.
"""


class put_in_same_family_controller(object):
    """ Class put_in_same_family_controller: the controller of the put in same familie view
    """  

    def __init__(self):
        """ Build a put_in_same_family_controller object defined by    
            view(type:cherrypy.Template)                     the put_in_same_familie view    
            model(type:ui.model.split_into_2families_model)  the put_in_same_familie model   
        """
        self.model = put_in_same_family_model()
    
    def __fill_template(self, user_id, project_id, params, view):
        """ Fill the put_in_same_family view by searching information into its model 
            params(type:{})    the dictionary of all the parameters given by the user
        """
        view.authkey = self.model.get_authkey(user_id, project_id)
        view.putative_rnas = self.model.get_putative_rnas(params)
        view.mount_point = self.model.get_mount_point()
        
    @cherrypy.expose
    def index(self, **params):
        """ index page of put_in_same_family
            **params(type:{})    the dictionary of all the parameters given by the user
        """
        mount_point = self.model.get_mount_point()
        view = common.get_template('explore/put_in_same_family_view.tmpl')
        if params.has_key("authkey"):
            [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
            if user_id is None or project_id is None:
                return self.error(AUTH_ERROR)
            # If the user has data on the disk
            if self.model.user_has_data(user_id): 
                if self.model.get_action(params) == "put_in_same_family":
                    try:
                        self.model.put_in_same_family(user_id, project_id,
                                                      params)
                        return ""
                    except disk_error, error:
                        authkey = self.model.get_authkey(user_id, project_id)
                        url = mount_point + "explore/index?authkey=" + authkey
                        message = DISK_ERROR%url
                        return self.error(message, authkey)
                self.__fill_template(user_id, project_id, params, view)
                return view.respond()
            else:
                return "Your data have been deleted. For server maintenance, data are cleared after a while."
        else:
            return "You're not authorized to access this page."


    @cherrypy.expose
    def error(self, msg, authkey=None):
        error_page = error_controller()
        return error_page.get_page(msg, authkey)
