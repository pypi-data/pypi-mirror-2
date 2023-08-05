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
import os
import sys

from wrapper import wrapper

class mattygraph(wrapper):

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
        options = ''
        if self.opts != None:
            for opt in self.opts:
                if self.opts[opt] == "on":
                    options += '-' + opt + ' '
                elif self.opts[opt] != "off" and self.opts[opt] != "":
                    options += '-' + opt + ' "' + self.opts[opt] + '" '

        seq_path = self.get_sequence_file_path()

        blast_list = ""
        for blast in self.blast_paths:
            if os.path.isfile(blast):
                ftemp = open(blast, 'r')
                i = 0
                test = False
                for line in ftemp.readlines():
                    if i == 2:
                        test = True                    
                        break
                    i += 1
                if test:
                    ftemp.close()
                    blast_list += blast + ' '

        if blast_list != "":
            cmd = self.exe_path + ' -r "' + seq_path + '" -f "' +\
                ','.join(p for p in self.species_paths) + '" ' +\
                blast_list + '-d "' + self.gff_dir + '" ' + options

            self.launch(cmd)
        else:
            cmd = "mattygraph"
        t2 = time.clock()
        self.trace_predict_event(cmd,0,0,t2 - t1,"comparative_aggreg")


    def if_exec_error(self, retcode, cmd):
        if retcode != 0 and retcode != 1:
            mess = self.create_failed_message()
            self.trace_error_event(self.user_id, self.project_id, mess, cmd)
