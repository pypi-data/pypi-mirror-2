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


from rnaspace.ui.utils.common import common
from rnaspace.ui.model.error_model import error_model

class error_controller(object):
    """ Class error_controller: the controller of an error web page
    """
    
    def __init__(self):
        """ Build an error_controller object defined by    
            view(type:cherrypy.Template)      the error page view    
        """
        self.model = error_model()
        
    def get_page(self, msg, authkey=None):
        view = common.get_template('error_view.tmpl')
        
        view.authentification_platform = self.model.is_an_authentification_platform()
        view.content = msg
        view.authkey = authkey
        view.mount_point = self.model.get_mount_point()
        return str(view)
