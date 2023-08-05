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
import sys
import traceback

from rnaspace.ui.utils.common import common
from rnaspace.ui.controller.manage.manage_controller import manage_controller
from rnaspace.ui.controller.predict.predict_controller import predict_controller
from rnaspace.ui.controller.explore.explore_controller import explore_controller
from rnaspace.ui.controller.history_controller import history_controller
from rnaspace.ui.controller.help_controller import help_controller
from rnaspace.ui.model.rnaspace_model import rnaspace_model
from rnaspace.core.data_manager import data_manager
from rnaspace.core.email_sender import email_sender

import rnaspace.core.logger as logger

def handle_error():
    error = common.get_template('global_error.tmpl')
    cherrypy.response.status = 500
    (type, value, trace) = sys.exc_info()
    
    error_traceback = "An error occured !\n\n"
    if type is None and value is None:
        error_traceback = "no traceback :/"
    else:
        error_traceback = "\n".join(traceback.format_exception(type, value,
                                                               trace))
    data_m = data_manager()
    email_s = email_sender()
    email_s.send_admin_tb(error_traceback)
    error.authentification_platform = data_m.is_an_authentification_platform()
    error.mount_point = rnaspace_model().get_mount_point()
    cherrypy.response.body = str(error)


class rnaspace_controller(object):
    """ Class rnaspace_controller: the controller of the rnaspace home page
    """

    _cp_config = {'request.error_response':handle_error}
    
    def __init__(self):
        """ Build a rnaspace_controller object defined by    
            view(type:cherrypy.Template)                     the rnaspace home page   
            manage(type:ui.controller.manage_controller)     the manage page
            predict(type:ui.controller.predict_controller)   the predict page
            explore(type:ui.controller.explore_controller)   the explore page
        """
        logger.init()
        self.view = common.get_template('rnaspace_view.tmpl')
        self.cookie = common.get_template('cookies_error_view.tmpl')
        self.rnaspace_partners = common.get_template('rnaspace_partners.tmpl')
        self.predict = predict_controller()
        self.explore = explore_controller()      
        self.manage = manage_controller()
        self.history = history_controller()
        self.help = help_controller()
        self.model = rnaspace_model()
        
    @cherrypy.expose
    def index(self, **params):
        """ the rnaspace home page
        """
        if params.has_key("authkey"):
            [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
        else:
            user_id = None
            project_id = None
        self.view.user_active = self.model.is_user_active(user_id, project_id)
        self.view.user_has_done_a_run = self.model.has_user_done_a_run(user_id, project_id)
        self.view.authentification_platform = self.model.is_an_authentification_platform()
        if user_id != None and project_id != None:
            self.view.authkey = self.model.get_authkey(user_id, project_id)
        else:
            self.view.authkey = "None"            
        self.view.mount_point = self.model.get_mount_point()
        return self.view.respond()

    @cherrypy.expose
    def cookies_error(self):
        """ the rnaspace cookies error page
        """
        self.cookie.authentification_platform = self.model.is_an_authentification_platform()
        self.cookie.mount_point = self.model.get_mount_point()
        return self.cookie.respond()

    @cherrypy.expose
    def partners(self, **params):
        """ the rnaspace cookies error page
        """
        if params.has_key("authkey"):
            [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
        else:
            user_id = None
            project_id = None
        self.rnaspace_partners.user_active = self.model.is_user_active(user_id, project_id)
        self.rnaspace_partners.user_has_done_a_run = self.model.has_user_done_a_run(user_id, project_id)
        self.rnaspace_partners.authentification_platform = self.model.is_an_authentification_platform()
        if user_id != None and project_id != None:
            self.rnaspace_partners.authkey = self.model.get_authkey(user_id, project_id)
        else:
            self.rnaspace_partners.authkey = "None"
        self.rnaspace_partners.mount_point = self.model.get_mount_point()
        return self.rnaspace_partners.respond()
