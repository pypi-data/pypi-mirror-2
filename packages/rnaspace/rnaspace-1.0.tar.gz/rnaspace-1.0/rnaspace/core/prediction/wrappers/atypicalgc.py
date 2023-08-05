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
import time

from wrapper import wrapper
from rnaspace.core.putative_rna import putative_rna

class atypicalgc(wrapper):
    '''
    Identification of atypical G and C content regions.

    Approach:
    First, evaluate if the approach is appropriate (ie GC% mean on all the sequence
           is out [min_threshold ; max_threshold]
    If so, on each position of a given sequence, computes G and C percent content
    on a sliding window centered on the considered position.
    Only positions with a value more distant than two standard deviation
    of the mean are considered as atypical.
    Second, only regions (continuous atypical positions) longer than a minimum length are kept.

    Parameters:
    F: force prediction even if the approach is not appropriate
       Allowed values: True, False.
    T: only keep regions with GC% up/down/all mean value (with sliding window)
       Allowed values: 'up', 'down', 'all'
    W: sliding window size 
       Allowed values: integer value in [3 ; 501], if non odd integer, the value is reduced by 1
    L: minimum region length (integer value)
       Allowed values: integer value in [1 ; 500]
    Parameters values are not checked here.
    
    INRA BIA Toulouse, 2008
    '''

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

        result_file = self.get_temporary_file()
        sequence_file = self.get_sequence_file_path()

        opts = ''
        
        # get command line options
        if self.opts.has_key('F'):
            opts += '-F '
        opts += '-T ' + str(self.opts['T']) + ' '
        opts += '-W ' + str(self.opts['W']) + ' '
        opts += '-L ' + str(self.opts['L']) + ' '

        cmd = 'python %s %s %s %s' % (self.exe_path, opts ,sequence_file,
                                      result_file)
        self.launch(cmd)
        
        nb_predictions = self.memorize_results(result_file)
        
        t2 =  time.clock()
        self.trace_predict_event(cmd, nb_predictions, 0, t2-t1, "atypical")

    def memorize_results(self, result_file):

        if not os.path.isfile(result_file):
            return 0

        begin = 0
        end = 0
        rnas = []
        
        fresult = open(result_file, 'r')
        for line in fresult:
            if line.startswith('>'):
                (begin, end) = line[1:].split('|')
            else:
                rna_id = self.id_gen.get_new_putativerna_id(self.user_id,
                                                            self.project_id,
                                                            self.seq.id)
                prna = putative_rna(rna_id, self.seq.id, int(begin), int(end),
                                    self.run_id, user_id=rna_id, sequence=line,
                                    strand='.', domain=self.seq.domain,
                                    species=self.seq.species,
                                    strain=self.seq.strain,
                                    replicon=self.seq.replicon,
                                    score=0, program_name=self.program_name,
                                    program_version=self.program_version,
                                    day=self.day, month=self.month,
                                    year=self.year)
                rnas.append(prna)
        fresult.close()
        
        self.add_putative_rnas(rnas)
        
        return len(rnas)
        
