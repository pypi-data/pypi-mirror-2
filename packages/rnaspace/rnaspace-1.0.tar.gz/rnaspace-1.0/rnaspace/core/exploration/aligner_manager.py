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
import sys
import logging

from rnaspace.core.data_manager import data_manager
from rnaspace.core.trace.event import error_event
from rnaspace.core.email_sender import email_sender

class threads_manager:
    
    def __init__(self):
        self.threads = {}

        
    def add_thread(self, user_id, project_id, t):
        """ 
        add thread in running threads dictionnary

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        """
        self.threads.setdefault(user_id,{})
        self.threads[user_id].setdefault(project_id,[])
        self.threads[user_id][project_id].append(t)

    def run_threads_finished(self, user_id, project_id, name):
        """
        Return(type:boolean)   True if the execution of all selected
                               predictors has finished, False otherwise

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the id of the current run
        """
        try:
            for t in self.threads[user_id][project_id]:
                if t.getName() == name:
                    if t.isAlive():
                        return False
            return True
        except KeyError :
            return True


class aligner_manager:

    # running threads dictionary
    threads = None
    returned_values = {}
    
    def __init__(self):
        self.data_m = data_manager()
        self.logger = logging.getLogger("rnaspace")
        aligner_manager.threads = threads_manager()
        self.threads = aligner_manager.threads
        self.email_s = email_sender()

    def get_aligner_class(self, aligner, user_id, project_id):
        
        current = os.path.dirname(os.path.abspath(__file__))
        if os.path.abspath(current) not in sys.path:
            sys.path.append(os.path.abspath(current))
            
        # try to import the aligner  module
        try:        
            aligner_mod = __import__(aligner)
        except ImportError, error:
            message = "Module "+ aligner +".py not found." + "\n" + error.__str__()
            self.email_s.send_admin_tb(message)
            mail = self.data_m.get_user_email(user_id, project_id)
            ev = error_event(user_id, project_id, mail,
                            message, self.data_m.get_project_size(user_id, project_id))
            self.logger.error(ev.get_display())
            return None
            
        # try to get the aligner class
        try:
            aligner_class = getattr(aligner_mod, aligner)
        except AttributeError, error:
            message = "Class " + aligner + " not found in the module" + " " +\
                      aligner + ".py." + error.__str__()
            self.email_s.send_admin_tb(message)
            mail = self.data_m.get_user_email(user_id, project_id)
            ev = error_event(user_id, project_id, mail, 
                             message, self.data_m.get_project_size(user_id, project_id))
            self.logger.error(ev.get_display())
            return None

        return aligner_class
        
    def run_aligner(self, user_id, project_id, aligner, prnas):

        name = user_id + '_' + project_id + '_' + '_'.join(p for p in prnas)

        aligner_class = self.get_aligner_class(aligner, user_id, project_id)
        if aligner_class is not None:
            aligner_thread = aligner_class(user_id, project_id, prnas, name)
            aligner_thread.start()
            self.threads.add_thread(user_id, project_id, aligner_thread)
            return True
        else:
            return False

    def has_aligner_finished(self, user_id, project_id, prnas):
        name = user_id + '_' + project_id + '_' + '_'.join(p for p in prnas)
        return self.threads.run_threads_finished(user_id, project_id, name)

    def get_aligner_returned_value(self, user_id, project_id, prnas, aligner):
        name = user_id + '_' + project_id + '_' + '_'.join(p for p in prnas)
        return aligner_manager.returned_values[(name, aligner)]
