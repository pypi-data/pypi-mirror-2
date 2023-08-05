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
from rnaspace.ui.model.history_model import history_model

class history_controller(object):
    """ Class history_controller: the controller of the history page
    """
    
    def __init__(self):
        self.model = history_model()
        self.view = common.get_template('history_view.tmpl')

    @cherrypy.expose
    def index(self, **params):
        mount_point = self.model.get_mount_point()
        self.view.mount_point = mount_point

        if params.has_key("authkey"):
            [user_id, project_id] = self.model.get_ids_from_authkey(params["authkey"])
                  
            history = self.model.get_history(user_id, project_id)
            if history is not None:
                sorted_dates = history.keys()
                sorted_dates.sort(reverse=True)
                self.view.sorted_dates = sorted_dates
                self.view.history = history
            else:
                self.view.sorted_dates = None
                self.view.history = None
            return str(self.view)
        else:
            raise cherrypy.HTTPRedirect(mount_point + 'manage')
    
