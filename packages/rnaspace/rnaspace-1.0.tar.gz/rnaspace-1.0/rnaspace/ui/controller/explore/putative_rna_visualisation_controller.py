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
from rnaspace.ui.controller.popup_error_controller import popup_error_controller
from rnaspace.ui.model.explore.putative_rna_visualisation_model import putative_rna_visualisation_model
from rnaspace.ui.controller.error_controller import error_controller
from rnaspace.core.exceptions import disk_error


ADD_DISK_ERROR =\
"""
<br />
Sorry, no more space available. <br />
You can not add predictions.
<br /><br />
Return to <a href="%s">Explore page</a>.
"""

SAVE_DISK_ERROR =\
"""
<br />
Sorry, no more space available. <br />
You can not update this prediction.
<br /><br />
Return to <a href="%s">RNA visualisation page</a>.
"""

RNA_NOT_FOUND_ERROR =\
"""
<br />
Sorry, can not find the predictions you want to visualize. <br />
<br /><br />
Return to <a href="%s">Explore page</a>.
"""


class putative_rna_visualisation_controller(object):
    """ Class putative_rna_visualisation_controller: the controller of the rna visualisation popup
    """

    def __init__(self):
        """ Build a putative_rna_visualisation_controller object defined by    
            view(type:cherrypy.Template)                     the putative_rna_visualisation view     
        """
        self.model = putative_rna_visualisation_model()
        url = "/explore/rnavisualisation/index?authkey=%s&amp;mode=display&amp;rna_id=%s"
        self.rnavis_url = url
        
    def __fill_template(self, user_id, project_id, params, view):
        """ Fill the putative_rna_visualisation view by searching information into its model 
            **params(type:{})    the dictionary of all the parameters given by the user
        """
        mount_point = self.model.get_mount_point()
        view.authkey = self.model.get_authkey(user_id, project_id)
        view.mode = self.model.get_mode(params)
        view.rna_size_to_display = self.model.rna_size_to_display
        rna  = self.model.get_putative_rna(user_id, project_id, params)
        if rna is None:
            url =  mount_point + "explore/index?authkey=" + view.authkey
            return RNA_NOT_FOUND_ERROR % url
        view.save_rna = rna
        sequence = self.model.get_sequence(user_id, project_id, rna, params)
        if self.model.get_action(params) != "" and self.model.get_action(params) != "cancel_modification":
            rna = self.model.update_putative_rna(user_id, project_id, rna, sequence, params)

        view.putative_rna = rna
        view.genomical_context = self.model.get_genomical_context(sequence, rna)
        view.putative_rnas = self.model.get_rnas_to_merge(user_id, project_id, params)
        view.sequences_id = self.model.get_sequences_id(user_id, project_id, params)
        view.current_sequence_id = self.model.get_current_sequence_id(user_id, project_id, params)
        view.structures_picture = self.model.get_structures_picture(user_id, project_id, rna)
        view.predictors = self.model.predictors
        view.new_structure = self.model.get_new_structure(rna, params, user_id, project_id)
        view.genome_size = len(sequence.data)
        view.error = self.model.get_error_msg(params)
        view.ids_max_length = self.model.ids_max_length
        view.rna_names_already_used = self.model.get_rna_names_already_used(user_id, project_id)
        view.max_rna_size_for_structure_prediction = self.model.max_rna_size_for_structure_prediction
        view.mount_point = self.model.get_mount_point()
        return None

    def __error(self, msg):   
        """ Build an error page defined by a message error
            msg(type:string)   the message to display 
        """  
        error_page = popup_error_controller()
        return error_page.get_page(msg)

    @cherrypy.expose
    def picture(self, **params):
        (user_id, project_id) = (None, None)

        if params.has_key("authkey"):
            [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
        if user_id is None or project_id is None:
            return self.error(AUTH_ERROR)
        
        if not params.has_key("name"):
            return ""

        return self.model.get_structure_picture_content(params["name"])

    @cherrypy.expose
    def index(self, **params):
        """ index page of putative_rna_visualisation
            **params(type:{})    the dictionary of all the parameters given by the user
        """
        view = common.get_template('explore/putative_rna_visualisation_view.tmpl')
        mount_point = self.model.get_mount_point()
        if params.has_key("authkey"):
            [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
            if user_id is None or project_id is None:
                return self.error(AUTH_ERROR)
            # If the user has data on the disk
            if self.model.user_has_data(user_id): 
                #try:
                if self.model.get_action(params) == "save":
                    try:
                        rna_id = self.model.save_putative_rna(user_id,
                                                              project_id,
                                                              params)
                    except disk_error, error:
                        authkey = self.model.get_authkey(user_id, project_id)
                        rnaid = self.model.get_putative_rna(user_id,
                                                            project_id, params)
                        rnaid = rnaid.sys_id
                        url = self.rnavis_url%(authkey, rnaid)
                        message = SAVE_DISK_ERROR%url
                        return self.error(message, authkey)

                elif self.model.get_action(params) == "add":
                    try:
                        rna_id = self.model.add_putative_rna(user_id,
                                                             project_id,
                                                             params)
                        params["rna_id"] = rna_id
                        params["mode"] = "display"
                    except IOError, error:
                        params["error"] = error
                    except disk_error, error:
                        authkey = self.model.get_authkey(user_id, project_id)
                        url =  mount_point + "explore/index?authkey=" + authkey
                        message = ADD_DISK_ERROR%url
                        return self.error(message, authkey)             
                        
                msg = self.__fill_template(user_id, project_id, params, view)
                if msg is not None:
                    return self.error(msg, self.model.get_authkey(user_id, 
                                                                  project_id))
                return view.respond()
                #except:
                #    return self.__error("Error found when attempting to access the specified putative rna.")
            else:
                return self.__error("You're data have been deleted. For server maintenance, data are cleared after a while.")
        else:
            return self.__error("You're not authorized to access this page")

    @cherrypy.expose
    def error(self, msg, authkey=None):
        error_page = error_controller()
        return error_page.get_page(msg, authkey)
