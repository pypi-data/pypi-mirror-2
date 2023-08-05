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
import urlparse

from rnaspace.ui.utils.common import common, Error
from rnaspace.ui.utils.common import AUTH_ERROR
from rnaspace.ui.model.predict.predict_model import predict_model
from rnaspace.ui.controller.error_controller import error_controller
from rnaspace.ui.controller.infobar_controller import infobar_controller
from rnaspace.ui.controller.predict.parameters_controller import parameters_controller

           
class predict_controller:

    def __init__(self):
        self.model = predict_model()
        self.infobar = infobar_controller()
        self.parameters = parameters_controller()
  
    ############################################################################
    ## SESSION METHODS
    ##

    def init_session(self):
        cherrypy.session['selected_species'] = None
        cherrypy.session['checked_predictors'] = None
        cherrypy.session['level1_parameters'] = None
        cherrypy.session['level2_parameters'] = None
        cherrypy.session['selected_comp'] = None        
        cherrypy.session['error'] = Error()

    def reset_session(self):
        cherrypy.session['checked_predictors'] = None
        cherrypy.session['level1_parameters'] = None
        cherrypy.session['level2_parameters'] = None
        cherrypy.session['selected_comp'] = None
        cherrypy.session['selected_species'] = None

    def set_session(self, params):
        soft_opts = {}
        checked = {}
        for key in params:
            if key.endswith('_name'):
                name = '_'.join(s for s in key.split('_')[0:-2])
                type = key.split('_')[-2]
                checked.setdefault(type, [])
                checked[type].append(name)

            elif key.endswith('_option'):
                k = key.split('_')
                opt = '_'.join(o for o in k[0:-3])
                soft = k[-3]
                type = k[-2]
                soft_opts.setdefault(type,{})
                soft_opts[type].setdefault(soft,{})
                soft_opts[type][soft][opt] = params[key]
        cherrypy.session['checked_predictors'] = checked
        cherrypy.session['level1_parameters'] = soft_opts
        try:
            comp = {"inference":params['inf_soft'],
                    "conservation":params['cons_soft'],
                    "aggregation":params['agg_soft'],}
            cherrypy.session['selected_comp'] = comp
        except KeyError:
            cherrypy.session['selected_comp'] = None

    ############################################################################
    ## EXPOSED METHODS
    ##

    @cherrypy.expose
    def index(self, **params):
        view = common.get_template('predict/predict_view.tmpl')
        if not params.has_key("authkey"):
            return self.error("You're not authorized to access this page")

        self.init_session()
        
        (user_id,
         project_id) = self.model.get_ids_from_authkey(params["authkey"])
        if user_id is None or project_id is None:
            return self.error(AUTH_ERROR)

        sequences = self.model.get_nb_sequences(user_id, project_id)
        if sequences == 0:
            raise cherrypy.HTTPRedirect('/manage?authkey=' +
                                            params["authkey"])        
        view.authentification_platform =\
            self.model.is_an_authentification_platform()
        if view.authentification_platform:
            view.infobar = self.infobar.get_infobar(user_id, project_id)
            
        done_a_run = self.model.has_user_done_a_run(user_id, project_id)
        view.user_has_done_a_run = done_a_run
        view.authkey = params["authkey"]        
        view.known_softs = self.model.get_software_by_type("known")
        view.abinitio_softs = self.model.get_software_by_type("abinitio")
        view.inf_softs = self.model.get_software_by_type("inference")
        view.agg_softs = self.model.get_software_by_type("aggregation")
        view.cons_softs = self.model.get_software_by_type("conservation")
        view.selected = cherrypy.session['selected_comp']
        view.dbnames = self.model.get_db_names(user_id, project_id)
        view.species = self.model.get_species_names()
        view.selected_species = cherrypy.session['selected_species']
        view.checked_softs = cherrypy.session["checked_predictors"]
        view.updated = cherrypy.session['level1_parameters']
        comp_part = self.model.comparative_activated(user_id, project_id)
        view.comparative_part = comp_part
        view.known_part = self.model.known_activated(user_id, project_id)
        view.abinitio_part = self.model.abinitio_activated(user_id,
                                                           project_id)
        view.mount_point = self.model.get_mount_point()
        return str(view)
                
    @cherrypy.expose
    def submit(self, **params):        
        """
        Return(type:string)     the "wait" page                
        """

        wait_view = common.get_template('predict/wait_view.tmpl')
        (user_id,
         project_id) = self.model.get_ids_from_authkey(params["authkey"])
        if user_id is None or project_id is None:
            return self.error(AUTH_ERROR)

        try:
            self.set_session(params)
        except:
            self.init_session()
            self.set_session(params)

        for param in params:
            # ask for a parameter page
            if param.startswith('param_button_'):
                # memorize selected species
                if params.has_key('species_names'):
                    cherrypy.session['selected_species'] = params['species_names']
                else:
                    cherrypy.session['selected_species'] = None

                # redirect to parameters page
                mount_point = self.model.get_mount_point()
                p = param.split('_')
                page = mount_point + 'predict/parameters/index?soft=' + p[3] +\
                    '&amp;type=' + p[2] + "&amp;authkey=" + params["authkey"]
                raise cherrypy.HTTPRedirect(page)

        # the run button has been clicked
        run_id = self.model.new_run(user_id, project_id)
        level1 = cherrypy.session['level1_parameters']
        level2 = cherrypy.session['level2_parameters']
        # launch predictors
        self.model.launch_software(user_id, project_id, run_id, params, level1,
                                   level2)

        # reset the session and fill the wait page
        self.reset_session()
        wait_view.mount_point = self.model.get_mount_point()
        wait_view.authkey = params["authkey"]
        wait_view.id = project_id
        wait_view.run_id = run_id
        mount_point = self.model.get_mount_point()
        wait_view.url = mount_point +"predict/wait?authkey=" + params["authkey"]
        wait_view.email = self.model.get_user_email(user_id, project_id)
        wait_view.authentification_platform = self.model.is_an_authentification_platform()

        return str(wait_view)

    @cherrypy.expose
    def wait(self, **params):
        
        wait_view = common.get_template('predict/wait_view.tmpl')
        job_failed = common.get_template('predict/job_failed.tmpl')
        
        (user_id,
         project_id) = self.model.get_ids_from_authkey(params["authkey"])
        if user_id is None or project_id is None:
            return self.error(AUTH_ERROR)

        run_id = params['run']
        email = self.model.get_user_email(user_id, project_id)

        # if run not finished, display the wait page
        if not self.model.run_finished(user_id, project_id, run_id):            
            mount_point = self.model.get_mount_point()
            wait_view.mount_point = mount_point
            wait_view.authkey = params["authkey"]
            wait_view.id = project_id
            wait_view.run_id = run_id
            wait_view.url = mount_point + "predict/wait?authkey=" + params["authkey"]
            if email is not None:
                wait_view.email = email
            wait_view.authentification_platform = self.model.is_an_authentification_platform()
            return str(wait_view)
          
        # if run failed, display an error page
        failed_soft = self.model.run_failed(user_id, project_id, run_id)
        if len(failed_soft) != 0 :
            mount_point = self.model.get_mount_point()
            url = cherrypy.server.base()
            url = urlparse.urljoin(url, mount_point +'explore/index?authkey=' +\
                                       params["authkey"] + "&predict=True")
            job_failed.url = url
            job_failed.predictors = failed_soft                
            return self.error(str(job_failed), params['authkey'])
                
        # redirect user to explore page
        mount_point = self.model.get_mount_point()
        raise cherrypy.HTTPRedirect(mount_point + 'explore/index?authkey=' + 
                                    params["authkey"] + "&predict=True")

    @cherrypy.expose
    def error(self, msg, authkey=None):
        error_page = error_controller()
        return error_page.get_page(msg, authkey)


