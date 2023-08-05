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
from rnaspace.ui.model.predict.parameters_model import parameters_model
from rnaspace.ui.controller.infobar_controller import infobar_controller
from rnaspace.ui.controller.error_controller import error_controller

class parameters_controller:

    def __init__(self):
        self.model = parameters_model()
        self.infobar = infobar_controller()


    ############################################################################
    ## EXPOSED METHODS
    ##

    @cherrypy.expose
    def error(self, msg, authkey=None):
        error_page = error_controller()
        return error_page.get_page(msg, authkey)

    @cherrypy.expose
    def index(self, **params):               
        """
        Return(type:string)    parameters page for a software

        params:
          soft(string)         name of the software
          type(string)         can be 'known', 'conservation', 'aggregation',
                               'inference' or 'abinitio'
          mode(string)         can be 'expert' or 'basic'
        """

        param_view = common.get_template('predict/param_view.tmpl')

        if not params.has_key("authkey"):
            return self.error("You're not authorized to access this page")
        if not cherrypy.session.has_key('param_error'):
            cherrypy.session['param_error'] = {}
        if not cherrypy.session.has_key('level2_parameters'):
            cherrypy.session['level2_parameters'] = None

        (user_id,
         project_id) = self.model.get_ids_from_authkey(params["authkey"])
        if user_id is None or project_id is None:
            return self.error(AUTH_ERROR)
        softname = params['softname']
        softtype = params['type'].split('_')[0]

        updated = cherrypy.session['level2_parameters']

        param_error = cherrypy.session['param_error']
        
        soft = self.model.get_software(softname, softtype)
        
        authentification_platform = self.model.is_an_authentification_platform()
        param_view.authentification_platform = authentification_platform
        param_view.authkey = params["authkey"]
        param_view.user_has_done_a_run =\
            self.model.has_user_done_a_run(user_id, project_id)

        param_view.predictor = soft
        param_view.updated = updated        
        param_view.param_error = param_error
        param_view.mount_point = self.model.get_mount_point()
        return str(param_view)


    @cherrypy.expose
    def submit(self, **params):
        (user_id,
         project_id) = self.model.get_ids_from_authkey(params["authkey"])
        if user_id is None or project_id is None:
            return self.error(AUTH_ERROR)

        previous = "/predict?authkey=" + params["authkey"]
        softname = params['softname']
        softtype = params['type'].split('_')[0]

        param_page = "/predict/parameters?authkey=" + params["authkey"]
        param_page += "&amp;softname=%s&amp;type=%s"%(softname, softtype)

        if 'cancel_param' in params.keys():
            cherrypy.session['param_error'] = {}
            return ""

        if 'default_param' in params.keys():  
            try:
                cherrypy.session['level2_parameters'][softtype][softname] = None
            except:
                pass
            
            raise cherrypy.HTTPRedirect(param_page)

        p = self.model.get_opts(params)

        # we first check if parameter are ok
        cherrypy.session['param_error'] = self.model.check_param(softname,
                                                                 softtype, p)

        # if not, write an error and return to the parameters page
        if len(cherrypy.session['param_error']) > 0:
            raise cherrypy.HTTPRedirect(param_page)

        # if yes, then we update the command line and we go to predict
        if cherrypy.session['level2_parameters'] is None:
            cherrypy.session['level2_parameters'] = {}

        cherrypy.session['level2_parameters'].setdefault(softtype, {})
        cherrypy.session['level2_parameters'][softtype][softname] = p

        return ""

