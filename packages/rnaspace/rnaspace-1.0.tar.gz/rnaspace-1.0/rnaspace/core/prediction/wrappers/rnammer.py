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
import re

from wrapper import wrapper
from rnaspace.core.putative_rna import putative_rna

class rnammer(wrapper):

    def __init__(self, opts, seq, user_id, project_id, run_id, p, stderr, stdout,
                 program_name, type, thread_name, version, exe):
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
        '''Run rnammer gene finder for selected rRNA subunits.
        
        The value of the 'S' parameter in opts indicates the sequence domain.
        The value of the 'm' parameter in opts indicates the lists of rRNA subunits to search for.
        Available values for this list are 'tsu', 'lsu' and 'ssu'. Each values of the list has to be splited 
        by a coma like 'lsu, tsu, ssu'.
        '''
        
        t1 = time.clock()
        search_opt = ' '
        if self.seq.is_bacteria():
            search_opt = ' -S bac '
        elif self.seq.is_archaea():
            search_opt = ' -S arc '
        elif self.seq.is_eukaryote():
            search_opt = ' -S euk '
        else: # If nothing is linked, let's run the bac profile by default
            search_opt = ' -S bac '
        
        options = ''
        if self.opts is not None:
            options += "-m "
            for opt in self.opts:
                if self.opts[opt] != '':
                    if self.opts[opt] == 'True':
                        options += opt + ','
            options = options[0:len(options)-1] + " "

        result = self.get_temporary_file()
        cmd = self.exe_path + search_opt + options + '-T ' + self.get_temporary_directory() + ' -gff ' + result + " " + self.get_sequence_file_path()
        self.launch(cmd)
        [nb_prediction, nb_alignment]=self.memorize_results(result)
        t2 = time.clock()
        self.trace_predict_event(cmd,nb_prediction,nb_alignment,t2 - t1,"rnammer")


    def memorize_results(self, result_file):
        """
        Convert the RNA predictions text file in an RNA objects and store them.
        """

        prnas_list = []
        fss = open(result_file, 'r')
        for line in fss.readlines():            
            if not re.search("^#", line):
                fields = line.rstrip().split()
                id = self.id_gen.get_new_putativerna_id(self.user_id, 
                                                        self.project_id,
                                                        self.seq.id)
                prnas_list.append(putative_rna(id, self.seq.id, int(fields[3]),\
                                               int(fields[4]), self.run_id, user_id=id, family=fields[8],\
                                               sequence=self.seq.data[int(fields[3])-1:int(fields[4])], strand=fields[6],\
                                               domain=self.seq.domain, species=self.seq.species,\
                                               strain=self.seq.strain, replicon=self.seq.replicon,\
                                               score=float(fields[5]), program_name=self.program_name,\
                                               program_version=self.program_version, day=self.day,\
                                               month=self.month, year=self.year))
        self.add_putative_rnas(prnas_list)
        fss.close()
        return [len(prnas_list),0]
