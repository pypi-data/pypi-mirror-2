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
from rnaspace.ui.model.manage.manage_model import manage_model
from rnaspace.ui.controller.error_controller import error_controller
from rnaspace.ui.controller.infobar_controller import infobar_controller
from rnaspace.core.exceptions import disk_error

DISK_ERROR =\
"""
<br />
Sorry, no more space available. <br />
You can not upload these sequences.
<br /><br />
Return to <a href="%s">Load page</a>.
"""


class manage_controller:
    """ Class manage_controller: the controller of the manage web page
    """

    def __init__(self):
        """ Build a manage_controller object defined by    
            view(type:cherrypy.Template)           the manage page view    
        """

        self.model = manage_model()
        self.infobar = infobar_controller()

    def __fill_template(self, user_id, project_id, params, view):
        """ Fill the manage view by searching information into its model 
            params(type:{})    the dictionary of all the parameters given by the user
        """
        view.authentification_platform = self.model.is_an_authentification_platform()
        if view.authentification_platform:
            view.infobar = self.infobar.get_infobar(user_id, project_id)
            putative_rnas = self.model.get_putative_rnas(user_id, project_id)
            view.putative_rnas = putative_rnas
            runs = []
            for run in putative_rnas.keys():
                runs.append(run)
            runs = sorted(runs)
            view.runs = runs
            view.alignments = self.model.get_alignments(user_id, project_id)
        view.available_domain = self.model.available_domain
        view.sequences = self.model.get_project_sequences(user_id, project_id)
        view.headers = self.model.get_project_sequences_header(user_id, project_id)
        view.sample_sequence = self.model.get_sample_sequence(params)
        view.current_seq_id = self.model.get_current_sequence_id(user_id, project_id)
        view.sequence_size_limitation = self.model.get_sequence_size_limitation()
        view.nb_sequences_limitation = self.model.get_nb_sequences_limitation()
        view.error = self.model.get_error_msg(params)
        view.last_action = self.model.get_action(params)
        view.unknown_user = self.model.get_unknown_user_name()
        view.authkey = self.model.get_authkey(user_id, project_id)
        view.mount_point = self.model.get_mount_point()

    @cherrypy.expose
    def index(self, **params):
        """ index page of manage
        """

        view = common.get_template('manage/manage_view.tmpl')
        if params.has_key("authkey"):
            [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
            if user_id is None or project_id is None:
                return self.error(AUTH_ERROR)
        else:
            user_id = self.model.get_unknown_user_name()
            project_id = self.model.create_new_project(user_id)

        mount_point = self.model.get_mount_point()

        if self.model.get_action(params) == "add_sequence":
            try:
                self.model.add_sequences(user_id, project_id, params)
            except ImportError, error:
                params["error"] = error
            except KeyError, error:
                params["error"] = error
            except IOError, error:
                params["error"] = error
            except disk_error, error:
                url = mount_point + "manage/index"
                message = DISK_ERROR%url
                return self.error(message)
                
        elif self.model.get_action(params) == "configure_predictors":
            self.model.save_user_email(user_id, project_id, params)
            id = self.model.get_authkey(user_id, project_id)
            raise cherrypy.HTTPRedirect(mount_point + 'predict/index?authkey='+id)
    
        self.__fill_template(user_id, project_id, params, view)
        return view.respond()
        

    @cherrypy.expose
    def error(self, msg, authkey=None):
        error_page = error_controller()
        return error_page.get_page(msg, authkey)
