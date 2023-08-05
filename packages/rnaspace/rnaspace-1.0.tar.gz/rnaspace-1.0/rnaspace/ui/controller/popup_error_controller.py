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

class popup_error_controller(object):
    """ Class popup_error_controller: the controller of an error popup
    """
    
    def __init__(self, msg):
        """ Build an popup_error_controller object defined by    
            view(type:cherrypy.Template)      the popup_error view    
        """
        self.view = common.get_template('popup_error_view.tmpl')
        self.view.content = msg
        
    def get_page(self):
        return str(self.view)
