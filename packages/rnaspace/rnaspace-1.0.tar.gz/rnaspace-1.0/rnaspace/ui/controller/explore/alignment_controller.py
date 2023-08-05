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
import urllib

from rnaspace.ui.utils.common import common
from rnaspace.ui.utils.common import AUTH_ERROR
from rnaspace.ui.controller.error_controller import error_controller
from rnaspace.ui.model.explore.alignment_model import alignment_model
from rnaspace.core.exceptions import disk_error

DISK_ERROR =\
"""
<br />
Sorry, no more space available. <br />
You can not save alignments.
<br /><br />
Return to <a href="%s">Alignment page</a>.
"""

ALIGNER_ERROR =\
"""
<br />
Sorry, an error occured during the alignment execution. <br />
An email has been sent to the administrator.
<br /><br />
Return to <a href="%sexplore/index?authkey=%s">Explore page</a>.
"""


class alignment_controller(object):
    """ Class allignment_controller: the controller of the allignement view
    """

    def __init__(self):
        """ Build a allignement_controller object defined by    
            view(type:cherrypy.Template)    the allignment view     
        """
        self.model = alignment_model()

    def __error(self, msg, authkey=None):   
        """ Build an error page defined by a message error
            msg(type:string)   the message to display 
        """  
        error_page = error_controller()
        return error_page.get_page(msg, authkey)

    @cherrypy.expose
    def picture(self, **params):
        (user_id, project_id) = (None, None)

        if params.has_key("authkey"):
            [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
        if user_id is None or project_id is None:
            return self.__error("You're not authorized to access this picture")
        
        if not params.has_key("name"):
            return ""

        return self.model.get_structure_picture_content(params["name"])

    @cherrypy.expose
    def index(self, **params):

        if not params.has_key("authkey"):
            return self.__error("You're not authorized to access this page")
        
        view = common.get_template('explore/alignment_view.tmpl')
        [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
        if user_id is None or project_id is None:
            return self.__error(AUTH_ERROR)
        # If the user has data on the disk
        if not self.model.user_has_data(user_id): 
            return self.__error("You're data have been deleted. " +
                                "For server maintenance, data are " +
                                "cleared after a while.", params['authkey'])

        if self.model.get_mode(params) == "display":
            try:
                page_number = params["page_number"]
            except:
                page_number = "1"
            align_ids = self.model.get_alignments_ids(params)
            nb_pages = int((len(align_ids)-1)/10) + 1
            align_ids.sort()
            align_ids = align_ids[(int(page_number)-1)*10:int(page_number)*10]
            mount_point = self.model.get_mount_point()
            aligns = self.model.get_colored_alignments(user_id, project_id,
                                                       align_ids, mount_point)
            try:
                if params["bad"] == "True":
                    view.bad = True
                else:
                    view.bad = False
            except:
                view.bad = False
            view.aligns = aligns
            view.mode = "display"
            view.nb_pages = str(nb_pages)
            view.page = page_number
            view.prna_id= ""
            view.project_id = project_id
            view.authkey = params["authkey"]
            view.max_item_length = self.model.max_item_length
            view.mount_point = self.model.get_mount_point()
            return str(view)

        if self.model.get_mode(params) == "display_all":
            prna_id = params["prna_id"]
            page_number = params["page_number"]
            align_ids = self.model.get_alignments_ids_for_prna(user_id,
                                                               project_id,
                                                               prna_id)
            nb_pages = int((len(align_ids)-1)/10) + 1

            align_ids.sort()
            align_ids = align_ids[(int(page_number)-1)*10:int(page_number)*10]
            mount_point = self.model.get_mount_point()
            aligns = self.model.get_colored_alignments(user_id, project_id,
                                                       align_ids, mount_point)

            try:
                if params["bad"] == "True":
                    view.bad = True
                else:
                    view.bad = False
            except:
                view.bad = False
            view.aligns = aligns
            view.prna_id = prna_id
            view.mode = "display_all"
            view.nb_pages = str(nb_pages)
            view.page = page_number
            view.project_id = project_id
            view.authkey = params["authkey"]
            view.max_item_length = self.model.max_item_length
            view.mount_point = self.model.get_mount_point()
            return str(view)

        if self.model.get_action(params) == "save":
            url_params = {}
            url_params["mode"] = "display"
            url_params["project_id"] = project_id
            url_params["authkey"] = params["authkey"]
            
            try:
                new_align_id = self.model.save_alignments(user_id, project_id,
                                                          params)
            except disk_error, e:
                url_params["alignment0"] = params["alignment_to_save"]
                url_params["nb_alignments"] = 1
                url_params = urllib.urlencode(url_params)
                mount_point = self.model.get_mount_point()
                url = mount_point + "explore/alignment?" + url_params
                message = DISK_ERROR%url
                return self.__error(message, params["authkey"])
            
            url_params["alignment0"] = new_align_id[0]            
            align_ids = self.model.get_alignments_ids(params)
            for (i, align_id) in enumerate(align_ids):
                url_params["alignment" + str(i+1)] = align_id
            nb_align = len(url_params) - 1
            url_params["nb_alignments"] = str(nb_align)
            url_params = urllib.urlencode(url_params)
            mount_point = self.model.get_mount_point()
            page = mount_point + "explore/alignment?" + url_params
            raise cherrypy.HTTPRedirect(page)


        bad = str(not self.model.can_align(user_id, project_id, params))
        success = self.model.align_putative_rnas(user_id, project_id, params)
        if not success:
            mount_point = self.model.get_mount_point()
            message = ALIGNER_ERROR % (mount_point, params["authkey"])
            return self.__error(message, params["authkey"])
        
        params_string = urllib.urlencode(params)
        mount_point = self.model.get_mount_point()
        page = mount_point + "explore/alignment/wait?" + params_string + "&amp;bad=" + bad
        raise cherrypy.HTTPRedirect(page)

    @cherrypy.expose
    def wait(self, **params):
        mount_point = self.model.get_mount_point()
        wait_view = common.get_template('explore/alignment_wait.tmpl')
        [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
        if user_id is None or project_id is None:
                return self.__error(AUTH_ERROR)
        if not self.model.has_aligner_finished(user_id, project_id, params):
            params_string = urllib.urlencode(params)
            if params["bad"] == "True":
                wait_view.bad = True
            else:
                wait_view.bad = False
            wait_view.url = mount_point + "explore/alignment/wait?" + params_string
            wait_view.project_id = project_id
            wait_view.authentification_platform = self.model.is_an_authentification_platform()
            wait_view.mount_point = mount_point
            return str(wait_view)

        align_ids = self.model.get_aligner_returned_value(user_id, 
                                                          project_id,
                                                          params)
        if not align_ids:
            message = ALIGNER_ERROR % (mount_point, params["authkey"])
            return self.__error(message, params["authkey"])
        
        params_temp = {"nb_alignments":str(len(align_ids)), "mode":"display", 
                       "project_id":project_id, "authkey":params["authkey"],
                       "bad":params["bad"]}
        for (i, align_id) in enumerate(align_ids):
            params_temp["alignment" + str(i)] = align_id
        params_string = urllib.urlencode(params_temp)
        page = mount_point + "explore/alignment?" + params_string
        raise cherrypy.HTTPRedirect(page)

