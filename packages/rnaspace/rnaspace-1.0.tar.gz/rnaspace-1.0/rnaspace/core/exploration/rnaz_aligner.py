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
import subprocess
import time
import tempfile
import threading
import logging

from rnaspace.core.data_manager import data_manager
from rnaspace.core.alignment import alignment, alignment_entry
from rnaspace.core.id_tools import id_tools
from rnaspace.core.secondary_structure import secondary_structure
from rnaspace.core.putative_rna import putative_rna
from rnaspace.core.email_sender import email_sender
from rnaspace.core.trace.event import error_event
from rnaspace.core.exploration.aligner_manager import aligner_manager

class rnaz_aligner(threading.Thread):
    """ Class clustalw: in charge to execute clustalw and parse its result file
    """
    
    def __init__(self, user_id, project_id, prnas_id, thread_name):
        threading.Thread.__init__(self, name=thread_name)
        self.dm = data_manager()
        self.headers = {}
        self.project_id = project_id
        self.user_id = user_id
        self.prnas_id = prnas_id
        self.logger = logging.getLogger("rnaspace")


    def run(self):
        try:
            self.__run()
        except :
            import sys
            import traceback
            (type, value, trace) = sys.exc_info()
            message = "Problem running aligner rnaz_aligner" + \
                      "\n".join(traceback.format_exception_only(type, value))
            email_sender().send_admin_tb(message)
            mail = self.dm.get_user_email(self.user_id, self.project_id)
            ev = error_event(self.user_id, self.project_id, mail, 
                             message, self.dm.get_project_size(self.user_id, self.project_id))
            self.logger.error(ev.get_display())
    
    def __run(self):
        clustal_exe = self.dm.get_clustalw_exe()
        
        user_id = self.user_id
        project_id = self.project_id
        prnas_id = self.prnas_id
        prnas = []
        for prna_id in prnas_id:
            prna = self.dm.get_putative_rna(user_id, prna_id, project_id)
            prnas.append(prna)
        
        fasta = self.dm.create_export_file(user_id, project_id, prnas, "fasta")

        tmp_fasta = tempfile.NamedTemporaryFile().name
        clustal_result = tempfile.NamedTemporaryFile().name
        rnaz_res = tempfile.NamedTemporaryFile().name
        fstderr = tempfile.NamedTemporaryFile().name

        ftmpfasta = open(tmp_fasta, "w")
        ffasta = open(fasta, "r")
        i = 0
        for line in ffasta.readlines():
            if line.startswith('>'):
                name = line[1:]
                self.headers[i] = name.replace('\n', '')
                ftmpfasta.write('>' + str(i) + '\n')
                i = i + 1
            else:
                ftmpfasta.write(line)
        ftmpfasta.close()
        ffasta.close()
        os.remove(fasta)

        clustal_cmd = clustal_exe + ' -infile="' + tmp_fasta + '" -outfile="' +\
            clustal_result + '" -batch -outorder="infile" 1>/dev/null'
        
        stderr = open(fstderr,'w')
        retcode = subprocess.call(clustal_cmd, shell=True, stderr=stderr)
        stderr.close()
        os.remove(tmp_fasta)
        if retcode != 0:
            message = "Problem running aligner rnaz_aligner:" + clustal_cmd
            email_sender().send_admin_failed_email(self.user_id, self.project_id, \
                                                   "explore", "rnaz_aligner", clustal_cmd)
            mail = self.dm.get_user_email(self.user_id, self.project_id)
            ev = error_event(self.user_id, self.project_id, mail, 
                             message, self.dm.get_project_size(self.user_id, self.project_id))
            self.logger.error(ev.get_display())
            aligner_manager.returned_values[(self.getName(),
                                             "rnaz_aligner")] = None
        else:
            id_gen = id_tools()
            align_id = id_gen.get_new_alignment_id(user_id, project_id)

            rnaz_exe = self.dm.get_rnaz_exe()
            rnaz_cmd = rnaz_exe + ' -g -o ' + rnaz_res + ' ' + clustal_result

            stderr = open(fstderr,'w')
            retcode = subprocess.call(rnaz_cmd, shell=True)
            stderr.close()
            if retcode != 0:
                message = "Problem running aligner rnaz_aligner:" + rnaz_cmd
                email_sender().send_admin_failed_email(self.user_id, self.project_id, \
                                                       "explore", "rnaz_aligner", rnaz_cmd) 
                mail = self.dm.get_user_email(self.user_id, self.project_id)
                ev = error_event(self.user_id, self.project_id, mail, 
                                 message, self.dm.get_project_size(self.user_id, self.project_id))
                self.logger.error(ev.get_display())
                aligner_manager.returned_values[(self.getName(),
                                                 "rnaz_aligner")] = None
            else:
                align = self.__parse_rnaz_result(align_id, prnas, rnaz_res)
                aligner_manager.returned_values[(self.getName(),
                                                 "rnaz_aligner")] = align
                os.remove(rnaz_res)
                os.remove(clustal_result)
        

    def __parse_rnaz_result(self, align_id, prnas, rnaz_res):
        """
        Convert the RNA predictions text file in an RNA objects and store them.
        """

        # compute header for all prnas
        headers = {}
        for prna in prnas:
            headers[prna] = prna.user_id+"|"+prna.family
            if prna.domain != "":
                headers[prna] += "|" + prna.domain
            if prna.species != "":
                headers[prna] += "|" + prna.species
            if prna.strain != "":
                headers[prna] += "|" + prna.strain
            if prna.replicon != "":
                headers[prna] += "|" + prna.replicon
            headers[prna] += "|" + prna.strand + "|" +\
                str(prna.start_position) + "|" + str(prna.stop_position)

        # read result file
        fresult = open(rnaz_res, 'r')
        line_seq = False
        line_struc = False
        ali = []
        entries = []
        ali_seq = {}
        ali_struc = {}
        cons = None
        for line in fresult.readlines():
            if line.startswith(' SVM RNA-class'):
                score = float(line.split(' ')[-1])

            # header line
            if line.startswith('>'):
                line_seq = True
                current_seq = line[1:-1]

            # sequence line
            elif line_seq:
                seq = line.replace('\n', '')
                line_seq = False
                line_struc = True

            # structure line
            elif line_struc:
                struct = line.split()[0].replace('\n', '')
                try:
                    free_e = float(line.split()[2][:-1])
                except:
                    free_e = float(line.split()[1][1:])

                structure = secondary_structure('bracket', struct, "RNAz", free_e)
                line_struc = False

                if current_seq == 'consensus':                    
                    cons = putative_rna(id="consensus", 
                                        genomic_sequence_id="None", 
                                        start_position=-1, stop_position=-1, 
                                        run="explore", sequence=seq, 
                                        family="consensus", 
                                        structure=[structure], 
                                        program_name="clustalw + RNAz", 
                                        program_version="1.0", 
                                        day=str(time.localtime()[2]), 
                                        month=str(time.localtime()[1]), 
                                        year=str(time.localtime()[0]), 
                                        alignment=[align_id])

                    align = alignment(align_id, entries, "explore", cons,
                                      program_name="clustalw + RNAz",
                                      program_version="1.0",
                                      day=str(time.localtime()[2]), 
                                      month=str(time.localtime()[1]), 
                                      year=str(time.localtime()[0]),
                                      pvalue=score)
                else:
                    for prna in prnas:
                        if self.headers[int(current_seq)] == headers[prna]:
                            ali.append(prna)
                            ali_seq[prna.sys_id] = seq
                            ali_struc[prna.sys_id] = structure
                            a1 = alignment_entry(prna.sys_id, seq,
                                                 prna.start_position,
                                                 prna.stop_position,
                                                 prna.genomic_sequence_id,
                                                 structure, prna.replicon,
                                                 prna.domain, prna.species,
                                                 prna.strain, prna.strand)
                            entries.append(a1)
                            break

        fresult.close()
        return align
