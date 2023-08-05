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


import os.path
from Cheetah.Template import Template

ROOT = os.path.abspath(os.path.dirname(__file__))

AUTH_ERROR =\
"""
<br />
Sorry, invalid authentification key.
<br />
Return to <a href="/">Home page</a>
"""

class common (object):
    """ Class manage_controller: the controller of the manage web page
    """
    
    # the path to the template files
    template_path = '../view/'
    
    @staticmethod
    def get_template(template):
        """ Return(type:Cheetah.Template) the template given by the given path
            template(type:string)      path to the template
        """        
        fichier_tmpl = os.path.join(ROOT, common.template_path)
        fichier_tmpl = os.path.join(fichier_tmpl, template)
        template = Template(file = fichier_tmpl)   
        return template


class Error:

    def __init__(self, message=""):
        self.error_view = common.get_template('error.tmpl')
        self.message = message

    def html_message(self):      
        if self.message == "":
            return self.message
        else:
            self.error_view.message = self.message
            self.message = ""
            return str(self.error_view)

    def get_message(self):
        if self.message == "":
            return self.message
        else:
            temp = self.message
            self.message = ""
            return temp
