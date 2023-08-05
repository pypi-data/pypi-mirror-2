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

from wrapper import wrapper

class blast_conservation(wrapper):

    def __init__(self, opts, seq, user_id, project_id, run_id, p,
                 stderr, stdout, program_name, type, thread_name, version, exe):
        wrapper.__init__(self, opts, seq, user_id, project_id, run_id, p,
                         stderr, stdout, program_name, type, thread_name,
                         version, exe)

    def run(self):
        try:
            self.__run()
        except :
            import sys
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
        query_strands = {'both':'3', 'forward':'1', 'reverse':'2'}
        # construct options line
        options = ''
        if self.opts is not None:
            for opt in self.opts:
                if self.opts[opt] != '':
                    if opt == 'score':
                        l = self.opts[opt].replace(' ','').split(';')
                        match = l[0]
                        mismatch = l[1]
                        g = l[2]
                        e = l[3]
                        options += '-r ' + match + ' -q ' + mismatch +\
                            ' -G ' + g + ' -E ' + e + ' '
                    elif opt == 'S':
                        options += '-S ' + query_strands[self.opts[opt]] + ' '
                    elif opt == 'F':
                        if self.opts[opt] == "yes":
                            options += '-' + opt + ' T '
                        else:
                            options += '-' + opt + ' F '
                    else:
                        options += '-' + opt + ' ' + self.opts[opt] + ' '

        sequence_file = self.get_sequence_file_path()
        result_tmp = self.get_temporary_file()
 
        cmd = self.exe_path + ' -p blastn ' + options + '-D 1 -o ' +\
            result_tmp + ' -i ' + sequence_file + ' -j ' + self.db 

        self.launch(cmd)
        self.memorize_results(result_tmp)
        t2 = time.clock()
        self.trace_predict_event(cmd,0,0,t2 - t1,"comparative_align")


    def memorize_results(self, result_tmp):
        """
        Parse blast result file and write blast tabular files
        We need to do that because the tabular output( option -D 1) does not
        have the name of the reference sequence
        """

        ftabular = open(self.blast_path, 'w')
        finput = open(result_tmp, "r")
        result = finput.read().splitlines()
        finput.close()
        
        fdb = open(self.db, "r")
        dbcontent = fdb.read().splitlines()
        fdb.close()
        fseq = open(self.get_sequence_file_path(), "r")
        seqcontent = fseq.read().splitlines()
        fseq.close()

        query_name = seqcontent[0].replace(' ', '_').replace('\n', '')[1:]
        database_name = dbcontent[0].replace(' ', '_').replace('\n', '')[1:]

        for (i, line) in enumerate(result):
            if i > 2:
                l = line.split()
                l[0] = query_name
                l[1] = database_name
                ftabular.write('\t'.join(field for field in l) + '\n')
            else:
                ftabular.write(line + '\n')

        ftabular.close()
