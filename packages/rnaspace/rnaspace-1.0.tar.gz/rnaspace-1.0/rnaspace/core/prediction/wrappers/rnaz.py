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
from rnaspace.core.alignment import alignment
from rnaspace.core.alignment import alignment_entry

class rnaz(wrapper):

    def __init__(self, opts, seq, user_id, project_id, run_id, p, stderr, 
                 stdout, program_name, type, thread_name, version, exe, tools):

        wrapper.__init__(self, opts, seq, user_id, project_id, run_id, p, 
                         stderr, stdout, program_name, type, thread_name, 
                         version, exe, tools)
        # conversion tab for sequences headers
        self.headers_conv = {}
        self.seq_values = {}
        self.clustal = {}
        self.RNAZWINDOW = self.tools["rnazwindow"]
        self.CLUSTAL = self.tools["clustalw"]

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
        clustal_pattern = '^([0-9]+) +([\-a-zA-Z]+)$'
        clustal_line = re.compile(clustal_pattern)
        cmd = ""
        for file in self.fasta_files:
            t1 = time.clock()
            self.clustal = {}
            # we change headers in the fasta file because clustal truncate them
            fasta_temp = self.get_temporary_file()
            ftemp = open(fasta_temp, 'w')
            ffasta = open(file, 'r')
            i = 0
            for line in ffasta:
                if line.startswith('>'):
                    start = line.split()[1]
                    stop = line.split()[2]
                    strand = line.split()[3]
                    name = line.split()[0][1:]
                    self.headers_conv[i] = name
                    self.seq_values[i] =  (start, stop, strand)
                    ftemp.write('>' + str(i) + '\n')
                    i = i + 1
                else:
                    ftemp.write(line)
            ftemp.close()
            ffasta.close()

            # we first launch clustalw            
            clustalw = self.get_temporary_file()
            cmd = self.CLUSTAL + ' -infile="' + fasta_temp + '" -outfile="' + \
                clustalw + '" -batch -outorder="infile"'
            self.launch(cmd)

            # then we launch RNAz if the culstalw file is not empty
            cmd = "-"
            nb_prediction = 0
            nb_alignment = 0
            if os.path.isfile(clustalw) and not os.path.getsize(clustalw) == 0:
                # get the length of the alignment
                fclustal = open(clustalw, "r")
                clustal_content = fclustal.read()
                fclustal.close()
                length = 0
                for line in clustal_content.splitlines():
                    l = clustal_line.search(line)
                    if line.startswith("0"):
                        length += len(line) - 17
                    if l:
                        self.clustal.setdefault(l.group(1), "")
                        self.clustal[l.group(1)] += l.group(2).replace("\n", "")

                res = self.get_temporary_file()

                # if alignment > slice, we launch rnazWindow.pl before RNAz
                if length != 0:
                    if length > int(self.opts["slice"]):
                        rnazWindow_cmd = "perl " + self.RNAZWINDOW +\
                            " -w " + self.opts["window"]
                        rnazWindow_cmd += " -s " + self.opts["slice"] +\
                            " " + clustalw + " | "
                        cmd = rnazWindow_cmd + self.exe_path + ' -p ' +\
                            self.opts['p'] + " -b -g -o " + res
                    else:
                        cmd = self.exe_path + ' -p ' + self.opts['p'] +\
                            ' -b -g -o ' + res + ' ' + clustalw
                    self.launch(cmd)

                    [nb_prediction,
                     nb_alignment] = self.memorize_results(file, res)
                    t2 = time.clock()
                    self.trace_predict_event(cmd, nb_prediction,
                                             nb_alignment, t2 - t1,
                                             "comparative_infer")
            try:
                os.remove(res)
            except:
                pass

        # fake execution
        if len(self.fasta_files) == 0:
            t1 = time.clock()
            clustalw = self.get_temporary_file()
            res = self.get_temporary_file()
            cmd = self.exe_path + ' -p ' + self.opts['p'] +\
                  ' -b -g -o ' + res + ' ' + clustalw
            t2 = time.clock()
            self.trace_predict_event(cmd, 0, 0, t2 - t1, "comparative_infer")
            
        if len(self.prnas_to_add) > 0:
            self.add_putative_rnas(self.prnas_to_add)
            self.add_alignments(self.aligns_to_add)


    def memorize_results(self, input_file, result_file):
        """
        Convert the RNA predictions text file in an RNA objects and store them.
        """

        domain = self.seq.domain
        species = self.seq.species
        replicon = self.seq.replicon
        strain = self.seq.strain
        program_name = self.program_pipeline  
        seq_header = self.dm.get_sequence_header(self.user_id, self.project_id,
                                                 self.seq.id).replace(' ', '_')
        fresult = open(result_file, 'r')
        line_seq = False
        line_struc = False
        keep = False
        begin_rnazw = ""
        end_rnazw = ""
        ali_seq = {}
        entries = []
        cons = None
        rnazwindow = False
        prnas_to_add = []
        nb_prediction = 0
        nb_alignment = 0
        for line in fresult.readlines():
            if line.startswith(' Reading direction: forward'):
                align_id = self.id_gen.get_new_alignment_id(self.user_id,
                                                            self.project_id)
                strand1 = '+'

            if line.startswith(' Reading direction: reverse'):
                align_id = self.id_gen.get_new_alignment_id(self.user_id,
                                                            self.project_id)
                strand1 = '-'

            if line.startswith(' SVM RNA-class'):
                score = float(line.split(' ')[-1])

            # see if it is an arn or not
            if line.startswith(' Prediction:'):
                prediction = line.split(' ')[-1]
                if prediction == 'RNA\n':
                    keep = True
                else:
                    keep = False
                ref_num = 0

            # header line
            if line.startswith('>') and keep:
                line_seq = True
                if len(line[1:-1].split("/")) > 1:
                    current_seq = line[1:-1].split("/")[0]
                    rnazwindow = True
                    begin_rnazw = line[1:-1].split("/")[1].split('-')[0]
                    end_rnazw = line[1:-1].split("/")[1].split('-')[1]
                else:    
                    current_seq = line[1:-1]
                    rnazwindow = False
                    begin_rnazw = ""
                    end_rnazw = ""

            # sequence line
            elif line_seq and keep:
                seq = line.replace('\n', '')
                line_seq = False
                line_struc = True

            # structure line
            elif line_struc and keep:
                struct = line.split()[0].replace('\n', '')
                try:
                    free_e = float(line.split()[2][:-1])
                except:
                    free_e = float(line.split()[1][1:])

                structure = secondary_structure('bracket', struct,
                                                self.program_name, free_e)
                struct_no_gap = secondary_structure('bracket', 
                                                    struct.replace('-',''),
                                                    self.program_name, free_e)
                line_struc = False

                if current_seq != 'consensus':
                    (start, stop, strand) = self.seq_values[int(current_seq)]
                    if rnazwindow is True:
                        seq_clustal = self.clustal[current_seq]
                        seq_clustal_rnaz = seq_clustal[long(begin_rnazw):long(end_rnazw)]
                        seq_clustal_rnaz = seq_clustal_rnaz.replace("-", "")

                        start_rnazw = long(start) +\
                            len(seq_clustal[:long(begin_rnazw)].replace("-", ""))
                        stop_rnazw = start_rnazw + len(seq_clustal_rnaz)
                        start = str(start_rnazw)
                        stop = str(stop_rnazw)

                if current_seq == 'consensus':
                    
                    cons = putative_rna(id="consensus", 
                                        genomic_sequence_id=self.seq.id, 
                                        start_position=0, stop_position=0, 
                                        run=self.run_id, sequence=seq, 
                                        family="consensus", 
                                        structure=[structure], 
                                        program_name=self.program_name, 
                                        program_version=self.program_version, 
                                        day=self.day, month=self.month, 
                                        year=self.year, alignment=[align_id])

                    align = alignment(align_id, entries, self.run_id, cons,
                                      program_name="clustalW + RNAz",
                                      program_version="",
                                      day=self.day, month=self.month,
                                      year=self.year, pvalue=score)
                    
                    self.aligns_to_add.append(align)
                    nb_alignment = nb_alignment + 1

                    ali_seq = {}
                    entries = []
                    cons = None
                    ref_num = 0

                elif self.headers_conv[int(current_seq)] == seq_header:
                    id = self.id_gen.get_new_putativerna_id(self.user_id,
                                                            self.project_id,
                                                            self.seq.id)

                    p = putative_rna(id=id, genomic_sequence_id=self.seq.id, 
                                     start_position=long(start), 
                                     stop_position=long(stop)-1, 
                                     run=self.run_id, 
                                     sequence=seq.replace('-', ''),
                                     domain=domain,
                                     species=species,
                                     replicon=replicon,
                                     strain=strain,
                                     family=" ", strand=strand1, 
                                     structure=[struct_no_gap], 
                                     score=score,
                                     program_name=program_name, 
                                     day=self.day, month=self.month, 
                                     year=self.year, alignment=[align_id])

                    ali_seq[id] = seq
                    a1 = alignment_entry(id, seq, long(start), long(stop)-1,
                                         self.seq.id, structure, replicon,
                                         domain, species, strain, strand1)
                    entries.append(a1)
                    exist = False
                    for prna in prnas_to_add:
                        if (prna.start_position == p.start_position and
                            prna.stop_position == p.stop_position and
                            prna.genomic_sequence_id == p.genomic_sequence_id):
                            exist = True
                            if prna.strand == "-":
                                prna.structure = p.structure
                                prna.sequence = p.sequence
                            prna.strand = '.'
                            
                            break

                    if not exist:
                        prnas_to_add.append(p)

                        nb_prediction = nb_prediction + 1


                else:
                    (ref_name, 
                     ref_seq) = \
                     self.get_species_names(self.headers_conv[int(current_seq)])
                    spe = self.get_header_species_name(self.headers_conv[int(current_seq)])
                    
                    if ref_seq in ali_seq:
                        ref_seq_id = ref_seq+'_'+str(ref_num)
                        ali_seq[ref_seq+'_'+str(ref_num)] = seq
                        a1 = alignment_entry(ref_seq_id, seq, long(start),
                                             long(stop)-1, ref_name,
                                             structure, "", "", spe, strain,
                                             strand1)
                        entries.append(a1)


                    else:
                        ref_seq_id = ref_seq
                        ali_seq[ref_seq] = seq
                        a1 = alignment_entry(ref_seq, seq, long(start),
                                             long(stop)-1, ref_name,
                                             structure, "", "", spe, strain,
                                             strand1)
                        entries.append(a1)

                    ref_num +=1

        fresult.close()
        self.prnas_to_add.extend(prnas_to_add)
        return [nb_prediction, nb_alignment]
