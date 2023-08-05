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
import re

from wrapper import wrapper
from rnaspace.core.secondary_structure import secondary_structure
from rnaspace.core.putative_rna import putative_rna

class trnascanse(wrapper):

    def __init__(self, opts, seq, user_id, project_id, run_id, p, stderr, stdout,
                 program_name, type, thread_name, version, exe):
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
        '''Run trnascanse gene finder.
        
        The domain is specified using the 'B' paramter in opts for bacteria, 'A' for archaea,
        none of this mean eukaryote.
        The value of the 'C' parameter in opts indicates to use Cove analysis only.
        The value of the 'D' parameter in opts indicates to disable pseudogen checking.
        The value of the 'X' parameter in opts indicates the cutoff value.
        The value of the 'L' parameter in opts indicates the max length of tRNA intron + variable region.
        '''
        
        t1 = time.clock()
        options = ' '
        if self.seq.is_bacteria():
            options = ' -B '
        elif self.seq.is_archaea():
            options = ' -A '
        elif self.seq.is_eukaryote():
            pass # No option to set, Eukaryot by default
        else:
            options = ' -B '
            
        if self.opts.has_key('C'):
            if self.opts['C'] == 'True':
                options += ' -C '
        if self.opts.has_key('D'):
            if self.opts['D'] != 'True':
               options += ' -D '
        else:
            options += ' -D '
            
        options += ' -X '+ str(self.opts['X']) + ' -L '+ str(self.opts['L']) + ' '

        result = self.get_temporary_file()
        secondary_structures = self.get_temporary_file()
        sequence_file = self.get_sequence_file_path()

        cmd = self.exe_path + options + '-o ' + result + ' -f ' +\
            secondary_structures + ' ' + sequence_file

        self.launch(cmd)
        
        [nb_prediction, nb_alignment] = self.memorize_results(result, secondary_structures)
        os.remove(result)
        os.remove(secondary_structures)
        t2 = time.clock()
        self.trace_predict_event(cmd,nb_prediction,nb_alignment,t2 - t1,"trnascanse")


    def memorize_results(self, result_file, secondary_structures):
        """
        Convert the RNA predictions text file in an RNA objects and store them.
        """

        prnas_list = []

        fss = open(secondary_structures, 'r')
        first_line = True
        for line in fss.readlines():            

            if first_line:
                first_line = False
                pos = line.split()[1].split('-')
                start_pos = long(pos[0][1:])
                stop_pos = long(pos[1][:-1])
                if start_pos < stop_pos:
                    strand = '+'
                else:
                    strand = '-'
                    s = start_pos
                    start_pos = stop_pos
                    stop_pos = s
            elif re.search("Type:(.*)", line):
                type = line.split()[1]
                score = float(line.split()[8])
            elif re.search("Possible pseudogene:(.*)", line):
                type = "Pseudo"
            elif re.search("Seq: (.*)", line):
                seq = line.split()[1]

            elif re.search("Str: (.*)", line):
                struct = line.split()[1]

            if line == '\n':
                first_line = True
                id = self.id_gen.get_new_putativerna_id(self.user_id, 
                                                        self.project_id,
                                                        self.seq.id)
                struct = struct.replace('>', '(')
                struct = struct.replace('<', ')')
                structure = secondary_structure('bracket', struct,
                                                self.program_name, 0.0)
                if type == "Undet":
                    family = "tRNA"
                else:
                    family = "tRNA-" + type
                prnas_list.append(putative_rna(id, self.seq.id, start_pos,\
                                               stop_pos, self.run_id, user_id=id,\
                                               sequence=seq, family=family, strand=strand,\
                                               domain=self.seq.domain, species=self.seq.species,\
                                               strain=self.seq.strain, replicon=self.seq.replicon,\
                                               structure=[structure], score=score, program_name=self.program_name,\
                                               program_version=self.program_version, day=self.day,\
                                               month=self.month, year=self.year))
        self.add_putative_rnas(prnas_list)
        fss.close()
        return [len(prnas_list),0]
