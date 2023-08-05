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


import os
import re
import cherrypy
from cherrypy.lib import static


from rnaspace.core.exploration.filter import selection_criteria

from rnaspace.ui.utils.common import common
from rnaspace.ui.utils.common import AUTH_ERROR
from rnaspace.ui.model.explore.explore_model import explore_model
from split_into_2families_controller import split_into_2families_controller
from put_in_same_family_controller import put_in_same_family_controller
from putative_rna_visualisation_controller import putative_rna_visualisation_controller
from alignment_controller import alignment_controller
from sequence_visualisation_controller import sequence_visualisation_controller
from rnaspace.ui.controller.error_controller import error_controller
from rnaspace.ui.controller.infobar_controller import infobar_controller


class explore_controller(object):
    """ Class explore_controller: the controller of the explore web page
    """  

    def __init__(self):
        """ Build an explore_controller object defined by    
            view(type:cherrypy.Template)       the explore page view    
            model(type:ui.model.explore_model) the explore page model   
        """
        self.model = explore_model()
        self.splitinto2families = split_into_2families_controller()
        self.putinsamefamily = put_in_same_family_controller()
        self.rnavisualisation = putative_rna_visualisation_controller()
        self.alignment = alignment_controller()
        self.sequencevisualisation = sequence_visualisation_controller()
        self.infobar = infobar_controller()
        
    def __init_cookie(self, params):
        cookie = cherrypy.response.cookie
        cookie["current_page"] = self.model.get_current_page(params)
        cookie["sort_by"] = self.model.get_sort_by(params)
        cookie["ascent"] = self.model.get_sort_ascent(params)
        cookie["nb_putative_rnas_per_page"] = self.model.get_nb_putative_rnas_per_page(params)
        cookie["display_mode"] = self.model.get_display_mode(params)
        cookie["nb_criteria"] = 0
    
    def __update_filters_into_cookie(self, params):
        cookie = cherrypy.response.cookie
        cookie["current_page"] = self.model.get_current_page(params)
        cookie["sort_by"] = self.model.get_sort_by(params)
        cookie["ascent"] = self.model.get_sort_ascent(params)
        cookie["nb_putative_rnas_per_page"] = self.model.get_nb_putative_rnas_per_page(params)
        cookie["display_mode"] = self.model.get_display_mode(params)
        
        # First ask deletion of previous cookies
        for key in cherrypy.request.cookie.keys():
            if re.search("criteria.*", key) or re.search("operators.*", key) or re.search("value.*", key):
                cookie[key] = "todelete"
                cookie[key]['expires'] = 0
        
        # Then add brand new ones
        filters = self.model.get_filter_params(params)
        for key in filters.keys():
            cookie[key] = filters[key]
            cookie[key]['expires'] = 3600
        
    
    def __fill_template(self, user_id, project_id, params, view):
        """ Fill the explore view by searching information into its model 
            params(type:{})    the dictionary of all the parameters given by the user
        """
        
        view.authentification_platform = self.model.is_an_authentification_platform()
        if view.authentification_platform:
            view.infobar = self.infobar.get_infobar(user_id, project_id)
        
        arns = self.model.get_putative_rnas(user_id, project_id)
        if len(params) == 1:
            cookie = cherrypy.request.cookie
            if not cookie.has_key("current_page"):
                self.__init_cookie(params)
                cookie = cherrypy.response.cookie
            view.current_page = cookie["current_page"].value
            view.sort_by = cookie["sort_by"].value
            view.ascent = cookie["ascent"].value
            view.nb_putative_rnas_per_page = cookie["nb_putative_rnas_per_page"].value
            view.display_mode = cookie["display_mode"].value
            view.attributs_to_show = self.model.get_attributs_to_show(cookie["display_mode"].value)
            try:
                if params["predict"] == "True":
                    view.filter = self.model.get_filter_from_params(params) 
            except:
                    view.filter = self.model.get_filter_from_cookie(cookie)   
            view.putative_rnas = self.model.sort_and_filter_putative_rnas(arns, cookie, True)
        else:
            self.__update_filters_into_cookie(params)
            view.current_page = self.model.get_current_page(params)
            view.sort_by = self.model.get_sort_by(params)
            view.ascent = self.model.get_sort_ascent(params)
            view.nb_putative_rnas_per_page = self.model.get_nb_putative_rnas_per_page(params)
            display_mode = self.model.get_display_mode(params)
            view.display_mode = display_mode
            view.attributs_to_show = self.model.get_attributs_to_show(display_mode)
            view.filter = self.model.get_filter_from_params(params)  
            view.putative_rnas = self.model.sort_and_filter_putative_rnas(arns, params) 

        # Then others values
        view.runs_info = self.model.get_runs_info(user_id, project_id)
        view.len_all_rna = len(arns)
        view.project_id = project_id
        view.show_allowed = self.model.get_show_allowed()
        view.max_item_length = self.model.max_item_length
        view.available_combinaisons = selection_criteria.available_combinaisons
        view.all_attributs_name = self.model.get_all_attributs_name()
        view.sequences = self.model.get_project_sequences(user_id, project_id)
        view.headers = self.model.get_project_sequences_header(user_id, project_id)
        view.authkey = self.model.get_authkey(user_id, project_id)
        view.mount_point = self.model.get_mount_point()
        
    def __error(self, msg):   
        """ Build an error page defined by a message error
            msg(type:string)   the message to display 
        """  
        error_page = error_controller()
        return error_page.get_page(msg)

    @cherrypy.expose
    def index(self, **params):
        """ index page of explore
            **params(type:{})    the dictionary of all the parameters given by the user
        """
        view = common.get_template('explore/explore_view.tmpl')
        if params.has_key("authkey"):
            [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])        
            if user_id is None or project_id is None:
                return self.__error(AUTH_ERROR)
            if self.model.user_has_data(user_id, project_id): 
                #try:
                if self.model.get_action(params) == "delete":
                    self.model.delete_putative_rnas(user_id, project_id, params) 
                elif self.model.get_action(params) == "export":
                    path = self.model.create_export_file(user_id, project_id, False, params) 
                    return static.serve_file(path, "application/x-download", "attachment", os.path.basename(path))
                elif self.model.get_action(params) == "export_all":
                    path = self.model.create_export_file(user_id, project_id, True, params) 
                    return static.serve_file(path, "application/x-download", "attachment", os.path.basename(path))
                self.__fill_template(user_id, project_id, params, view)
                return view.respond()
                #except:
                #    return self.__error("An error occured, please contact the RNAspace team!")
            else:
                return self.__error("No data found for authkey = " + params["authkey"] + ", your datas may have been deleted (datas are deleted every " + self.model.get_project_expiration_days() + " days)")
        else:
            return self.__error("You're not authorized to access this page")


    @cherrypy.expose
    def get_cgview_file(self, **params):
        if params.has_key("authkey"):
            [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
            if user_id is None or project_id is None:
                return self.__error(AUTH_ERROR)
            if self.model.user_has_data(user_id, project_id):
                try:
                    return self.model.create_cgview_file(user_id, project_id, params)
                except IOError, error:
                    return error
            else:
                return self.__error("No data found for authkey = " + params["authkey"] + ", your datas may have been deleted (datas are deleted every " + self.model.get_project_expiration_days() + " days)")
        else:
            return self.__error("You're not authorized to access this page")

    @cherrypy.expose
    def tab_file(self, **params):
        (user_id, project_id) = (None, None)

        if params.has_key("authkey"):
            [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
        if user_id is None or project_id is None:
            return self.__error("You're not authorized to access this page")
        
        if not params.has_key("name"):
            return ""

        return self.model.tab_file_content(params['name'])
