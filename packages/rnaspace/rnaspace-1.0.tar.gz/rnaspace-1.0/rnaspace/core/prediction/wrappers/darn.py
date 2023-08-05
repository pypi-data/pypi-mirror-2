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

from wrapper import wrapper
from rnaspace.core.putative_rna import putative_rna
from rnaspace.core.secondary_structure import secondary_structure
from rnaspace.core.prediction.software_manager import software_manager

class darn(wrapper):

    def __init__(self, opts, seq, user_id, project_id, run_id, p, stderr, stdout,
                 program_name, type, thread_name, version, exe):
        wrapper.__init__(self, opts, seq, user_id, project_id, run_id, p, 
                         stderr, stdout, program_name, type, thread_name,
                         version, exe)
        
    # Naming in configuration file
    descriptors_conf_name = 'd'
    bacteria_letter = 'B'
    archaea_letter = 'A'
    eukaryote_letter ='E'

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
        '''Run darn gene finder for selected RNA family descriptor(s).

        The value of the 'd' parameter in opts indicates the RNA family descriptors to use.
        It contains one value of a list like: All [domain],FMN [B/A],Lysine [B/A/E] ...
        The first element indicates to use all the RNA family descriptors suitable to
        the request sequence domain.
        The other elements indicate a RNA family descriptor and the suitable domains
        (B for Bacteria, A for Archaea, E for Eukaryote).
        Note that it is not forbidden to use RNA family descriptor on a non domain suitable sequence.
        '''
        
        if self.opts is not None:
            for opt in self.opts:
                if opt == self.descriptors_conf_name:
                    descriptor_name = self.opts[opt].split()[0]
                    if descriptor_name == 'All':
                        sm=software_manager()
                        defined_descriptors = sm.get_options_params(self.program_name,
                                                                    self.type)[self.descriptors_conf_name]
                        
                        chosen_descriptors = []
                        # look for all descriptors of the corresponding sequence domain
                        for descriptor in defined_descriptors:
                            available_domains = descriptor.split()[1][1:-1].split('/')
                            if ((self.seq.is_bacteria()) and (self.bacteria_letter in available_domains)) or \
                               ((self.seq.is_archaea()) and (self.archaea_letter in available_domains)) or \
                               ((self.seq.is_eukaryote()) and (self.eukaryote_letter in available_domains)):
                                chosen_descriptors.append(descriptor.split()[0])
                    else:
                        chosen_descriptors = [descriptor_name]

        sequence_file = self.get_sequence_file_path()
        for descriptor in chosen_descriptors:
            t1 = time.clock()
            options = '-d ' + self.exe_path[0:len(self.exe_path)-len(os.path.basename(self.exe_path))-4] \
                      + 'descriptor/' + descriptor  + '.des'
        
            result = self.get_temporary_file()

            cmd = self.exe_path + ' -f P -n B ' + options + ' -s ' + sequence_file + ' -o ' + result 

            self.launch(cmd)
            [nb_prediction, nb_alignment] = self.memorize_results(result,descriptor)
            os.remove(result)
            t2 = time.clock()
            self.trace_predict_event(cmd,nb_prediction,nb_alignment,t2 - t1,"darn")


    def memorize_results(self, result_file, family):
        """
        Convert the RNA predictions text file in RNA objects and store them.
        """
        
        prnas_list = []
        nb_prediction = 0
        i = 0
        line1,line2 = None,None
        for line in open(result_file):
            if i==0: # one line in GFF
                line1 = line
                i += 1
            elif i==1: # one line sequence
                line2 = line
                i += 1
            else: # one line structure
                s = line1.split()
                start_pos = s[3]
                stop_pos = s[4]
                id = self.id_gen.get_new_putativerna_id(self.user_id,
                                                        self.project_id,
                                                        self.seq.id)

                strand = s[6]
                rna_seq = line2.replace('\n', '')
                structure = line.replace('\n', '')
                structure = secondary_structure('bracket', structure,
                                                self.program_name, 0.0)

                prnas_list.append(putative_rna(id, self.seq.id, long(start_pos),\
                                               long(stop_pos), self.run_id, user_id=id, family=family,\
                                               sequence=rna_seq, strand=strand,\
                                               domain=self.seq.domain, species=self.seq.species,\
                                               strain=self.seq.strain, replicon=self.seq.replicon,\
                                               structure=[structure], program_name=self.program_name,\
                                               program_version=self.program_version,\
                                               day=self.day, month=self.month, year=self.year))
                nb_prediction = nb_prediction + 1
                line1,line2 = None,None
                i = 0

        self.add_putative_rnas(prnas_list)
        return [nb_prediction,0]
        
