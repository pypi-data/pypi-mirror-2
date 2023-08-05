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

import time
import sys

from wrapper import wrapper

class yass_conservation(wrapper):

    def __init__(self, opts, seq, user_id, project_id, run_id, p,
                 stderr, stdout, program_name, type, thread_name, version, exe):
        wrapper.__init__(self, opts, seq, user_id, project_id, run_id, p,
                         stderr, stdout, program_name, type, thread_name,
                         version, exe)

    def run(self):
        try:
            self.__run()
        except :
            import traceback
            from rnaspace.core.trace.event import unknown_error_event
            (type, value, trace) = sys.exc_info()
            tb = "\n".join(traceback.format_exception(type, value, trace))
            error = "\n".join(traceback.format_exception_only(type, value))
            self.email_s.send_admin_tb(tb)
            ev = unknown_error_event(self.user_id, self.project_id, error,
                                     self.run_id, self.program_name)
            self.dm.update_project_trace(self.user_id, self.project_id, [ev])
            return

  
    def __run(self):

        t1 = time.clock()
        sequence_file = self.get_sequence_file_path()
        if self.opts == None:
            cmd = self.exe_path + ' -d 2 -o ' + self.blast_path + ' ' +\
                sequence_file + ' ' + self.db
        else:
                                
            # format options line
            options = ''
            gap_done = False

            for opt in self.opts:
                if opt == "E" or opt == "C" or opt == "p":
                    options = options + '-' + opt + ' "' + self.opts[opt] + '" '
                if opt == "e" and self.opts[opt] == "no":
                    options = options + '-e 0 '
                if (opt == "go" or opt == "ge") and not gap_done:
                    go = self.opts["go"]
                    ge = self.opts["ge"]
                    options = options + '-G "' + go + "," + ge + '" '
                    gap_done = True
                if opt == "r":
                    rvalues = {"both":"2", "forward":"0", "reverse":1}
                    options = options + " -r " + rvalues[self.opts[opt]] + " "
                if opt == "c":
                    cvalues = {"single":"1", "double":"2"}
                    options = options + " -c " + cvalues[self.opts[opt]] + " "
                    
            cmd = self.exe_path + ' ' + options + '-d 2 -o ' + self.blast_path +\
                ' ' + sequence_file + ' ' + self.db
            
        self.launch(cmd)    
        t2 = time.clock()
        self.trace_predict_event(cmd,0,0,t2 - t1,"comparative_align")

    def if_exec_error(self, retcode, cmd):
        ferr = open(self.stderr, 'r')
        err = ferr.read()
        ferr.close()
        if err.startswith("** ERROR"):
            mess = self.create_failed_message()
            self.trace_error_event(self.user_id, self.project_id, mess, cmd)
        
