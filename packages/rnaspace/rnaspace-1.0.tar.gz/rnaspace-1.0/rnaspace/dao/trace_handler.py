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

import threading
import os
try:
    import cPickle as pickle
except ImportError:
    import pickle

from storage_configuration_reader import storage_configuration_reader
from rnaspace.core.trace.project_trace import project_trace
    
class trace_handler (object):
    """ 
    Handler of project trace storage on a serialisation file
    """
    
    lock_trace = threading.Lock()
    trace_file = "trace.dump"


    def __init__(self):
        self.config = storage_configuration_reader()


    def __get_trace_file(self, user_id, project_id):
        """
        return serialised trace file
        """
        project_dir = self.config.get_project_directory(user_id, project_id)
        return os.path.join(project_dir, self.trace_file)

    def __get_trace(self, user_id, project_id):
        """
        user_id(type:string)           user identifier
        project_id(type:string)        project identifier
        return(type:project_trace)     current project trace
        """
        trace_file = self.__get_trace_file(user_id, project_id)
        if os.path.isfile(trace_file):
            f = open(trace_file, 'rb')
            trace = pickle.load(f)
            f.close()
        else:
            trace = project_trace()
        return trace

    def get_project_trace(self, user_id, project_id):
        """
        user_id(type:string)           user identifier
        project_id(type:string)        project identifier
        return(type:project_trace)     current project trace
        """
        self.lock_trace.acquire()
        trace = self.__get_trace(user_id, project_id)
        self.lock_trace.release()
        return trace

    def update_project_trace(self, user_id, project_id, events):
        """
        events(type:[event])      table of events to add to the trace
        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        """
        self.lock_trace.acquire()
        trace = self.__get_trace(user_id, project_id)
        for event in events:
            trace.add_events(event)
        
        trace_file = self.__get_trace_file(user_id, project_id)
        f = open(trace_file, 'wb')
        pickle.dump(trace, f)
        f.close()
        self.lock_trace.release()        
