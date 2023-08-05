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
from rnaspace.core.putative_rna import putative_rna

class erpin(wrapper):

    def __init__(self, opts, seq, user_id, project_id, run_id, p,
                 stderr, stdout, program_name, type, thread_name, version, exe):
        wrapper.__init__(self, opts, seq, user_id, project_id, run_id, p,
                         stderr, stdout, program_name, type, thread_name,
                         version, exe)
        self.erpin_dir = os.path.abspath(os.path.dirname(self.exe_path))

    def get_epn(self, epn_name):
        
        epn_dat = os.path.join(self.erpin_dir, "epn.dat")
        fepn_dat = open(epn_dat, 'r')
        for line in fepn_dat.readlines():
            l = line.split('//')
            if l[2] == epn_name:
                fepn_dat.close()
                return (l[0], l[-1])
        
        return (None, None)

    def run(self):
        try:
            self.__run()
        except Exception, e:
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
        '''Run erpin gene finder.
        
        Erpin parameters are gathered into a file epn.dat depending on the RNA family descriptors to use.
        It contains one value of a list like: All [domain], Archae 5S rRNA [A], Bacterial 5S rRNA [B] ...
        The first element indicates to use all the RNA family descriptors suitable to
        the request sequence domain.
        The other elements indicate a RNA family descriptor and the suitable domains
        (B for Bacteria, A for Archaea, E for Eukaryote, V for Virus).
        Note that it is not forbidden to use RNA family descriptor on a non domain suitable sequence.
        '''
        
        t1 = time.clock()
        epnscan_path = os.path.join(self.erpin_dir, "epnscan.pl")
        readerpin_path = os.path.join(self.erpin_dir, "readerpin.pl")

        result_epnscan = self.get_temporary_file()
        result_fasta = self.get_temporary_file()
        sequence_file = self.get_sequence_file_path()
        seq_copy = self.get_temporary_file()

        fseq_copy = open(seq_copy, 'w')
        fseq_file = open(sequence_file, 'r')
        fseq_copy.write(fseq_file.read().replace(' ', '_'))
        fseq_copy.close()
        fseq_file.close()

        if self.opts["training_set"] == "All [domain]":

            if self.seq.is_bacteria():
                domain = 'BAC'
            elif self.seq.is_archaea():
                domain = 'ARC'
            else:
                domain = 'EUK'

            # launch epnscan
            cmd = "perl " + epnscan_path + ' ' + seq_copy + ' ' + domain +\
                ' > ' +  result_epnscan

            self.launch(cmd)

        else:
            real_value = re.search("(.*) (\[[ABEV/]+\]$)", self.opts["training_set"])
            (epn, opt) = self.get_epn(real_value.group(1))
            cmd = self.exe_path + ' ' + os.path.join(self.erpin_dir, epn) +\
                ' ' + seq_copy + ' ' + opt.replace('\n', '') +\
                ' > ' + result_epnscan
            self.launch(cmd)
        cmd_memo = cmd   #only this command will be stored

        # launch readerpin
        cmd = "perl " + readerpin_path + ' -fasta < ' + result_epnscan +\
            ' > ' + result_fasta

        self.launch(cmd)
        [nb_prediction, nb_alignment]=self.memorize_results(result_fasta)
        os.remove(result_epnscan)
        os.remove(result_fasta)
        os.remove(seq_copy)
        t2 = time.clock()
        self.trace_predict_event(cmd_memo,nb_prediction,nb_alignment,t2 - t1,"erpin")

        
    def memorize_results(self, result):

        prnas_list = []

        fres = open(result, 'r')
        for line in fres.readlines():
            if line.startswith('>'):
                l = line.split()
                start_pos = l[-1].split('-')[0]
                stop_pos = l[-1].split('-')[1]
                strand = l[-2]
                family = ' '.join(car for car in l[1:-3])
                family = family.replace(' ','_')
            else:
                if strand == 'FW':
                    strand = '+'
                else:
                    strand = '-'

                seq = line.replace('\n', '')
                id = self.id_gen.get_new_putativerna_id(self.user_id, 
                                                        self.project_id,
                                                        self.seq.id)
                prnas_list.append(putative_rna(id, self.seq.id, 
                                               long(start_pos),
                                               long(stop_pos), self.run_id, 
                                               user_id=id, family=family,
                                               sequence=seq.replace('-', ''), 
                                               strand=strand,
                                               domain=self.seq.domain, 
                                               species=self.seq.species,
                                               strain=self.seq.strain, 
                                               replicon=self.seq.replicon,
                                               program_name=self.program_name,
                                               program_version=self.program_version,\
                                               day=self.day, month=self.month,
                                               year=self.year))

        self.add_putative_rnas(prnas_list)
        return [len(prnas_list),0]

