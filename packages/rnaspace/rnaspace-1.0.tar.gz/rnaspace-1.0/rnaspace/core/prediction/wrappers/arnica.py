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
import shutil
import glob
import re

from wrapper import wrapper
from rnaspace.core.secondary_structure import secondary_structure
from rnaspace.core.putative_rna import putative_rna
from rnaspace.core.alignment import alignment
from rnaspace.core.alignment import alignment_entry
from rnaspace.core.trace.event import error_event

class arnica(wrapper):

    def __init__(self, opts, seq, user_id, project_id, run_id, p, stderr,
                 stdout, program_name, type, thread_name, version, exe, tools):

        wrapper.__init__(self, opts, seq, user_id, project_id, run_id, p, 
                         stderr, stdout, program_name, type, thread_name, 
                         version, exe, tools)

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

        GARDENIA_EXE = self.tools["gardenia"]
        (GARDENIA_DIR, exe) = os.path.split(GARDENIA_EXE)
        GARDENIA_SCORE = os.path.join(GARDENIA_DIR, "score2.txt")

        # construct options line
        options = ' '
        if self.opts is not None:
            for opt in self.opts:
                if self.opts[opt] != '':
                    if opt == 'A':
                        if self.opts[opt] == "yes":
                            options += '-' + opt + ' '

        cmd = ""
        for file in self.fasta_files:
            t1 = time.clock()
            res_dir = self.get_temporary_directory()
            cmd = self.exe_path + options + '-C -o ' + res_dir + ' ' + file

            self.launch(cmd)
            
            if self.carnac_predict(res_dir):
                res_file = os.path.join(res_dir, 'carnac.out')

                gardenia_res = self.get_temporary_file()
                gardenia_cmd = GARDENIA_EXE + ' ' + res_file + ' -s --fasta -o '
                gardenia_cmd += gardenia_res + ' -S ' + GARDENIA_SCORE +\
                                ' 1>/dev/null 2>/dev/null' 
                os.system(gardenia_cmd)

                [nb_prediction,
                 nb_alignment]=self.memorize_results(file, gardenia_res)
                
                t2 = time.clock()
                self.trace_predict_event(cmd, nb_prediction, nb_alignment,
                                         t2-t1, "comparative_infer")

            else:
                nb_prediction = 0
                nb_alignment = 0

            try:
                shutil.rmtree(res_dir)
            except OSError:
                e = error_event(self.user_id,
                                self.project_id,
                                self.dm.get_user_email(self.user_id,
                                                       self.project_id),
                                "arnica shutil.rmtree error: " +
                                "Directory not empty ",
                                self.dm.get_project_size(self.user_id,
                                                         self.project_id)
                                )
                self.dm.update_project_trace(self.user_id, self.project_id, [e])
                

        # fake execution
        if len(self.fasta_files) == 0:
            t1 = time.clock()
            res_dir = self.get_temporary_directory()
            fas = self.get_temporary_directory()
            cmd = self.exe_path + options + '-C -o ' + res_dir + ' ' + fas
            t2 = time.clock()
            self.trace_predict_event(cmd, 0, 0, t2 - t1, "comparative_infer")


        if len(self.prnas_to_add) > 0:
            self.add_putative_rnas(self.prnas_to_add)
            self.add_alignments(self.aligns_to_add)
        


    def memorize_results(self, input_file, result_file):
        """
        Convert the RNA predictions text file in an RNA objects and store them.
        """

        prnas_list = []
        entries = []
        domain = self.seq.domain
        species = self.seq.species
        replicon = self.seq.replicon
        strain = self.seq.strain
        program_name = self.program_pipeline  
        i = 0
        line1,line2 = None,None
        gap_seq_struc = []
        try:
            rcontent = open(result_file)
        except:
            return [0, 0]

        for line in rcontent:
            if i==0: # one line in GFF
                line1 = line
                i += 1
            elif i==1: # one line sequence
                line2 = line
                i += 1
            else: # one line structure
                s = line1.split()
                name = s[0][1:]
                start_pos = s[1]
                stop_pos = s[2]
                h = self.dm.get_sequence_header(self.user_id, self.project_id,
                                                self.seq.id).replace(' ', '_')
                (ref_name, ref_seq) = self.get_species_names(name)

                if name == h:
                    id = self.id_gen.get_new_putativerna_id(self.user_id,
                                                            self.project_id,
                                                            self.seq.id)
                    gsid = self.seq.id
                else:
                    id = "%" + name
                    gsid = ref_name

                strand = "."
                rna_seq = line2.replace('\n', '').replace('-', '')
                gap_rna_seq = line2.replace('\n', '')
                structure = line.replace('\n', '').replace('-', '')
                structure = secondary_structure('bracket', structure,
                                                self.program_name, 0.0)
                gap_structure = line.replace('\n', '')
                gap_structure = secondary_structure('bracket', gap_structure,
                                                    self.program_name, 0.0)
                
                if structure.structure.find("(") != -1:
                    
                    a1 = alignment_entry(id, gap_rna_seq, long(start_pos),
                                         long(stop_pos)-1, gsid, gap_structure,
                                         replicon, domain, species, strain,
                                         strand)
                    entries.append(a1)    
                    
                    prna = putative_rna(id=id, 
                                        genomic_sequence_id=self.seq.id, 
                                        start_position=long(start_pos),
                                        stop_position=long(stop_pos)-1, 
                                        run=self.run_id,
                                        sequence=rna_seq,
                                        domain=domain,
                                        species=species,
                                        replicon=replicon,
                                        strain=strain,
                                        strand=strand, 
                                        structure=[structure],
                                        score=0.0, 
                                        program_name=program_name, 
                                        day=self.day, 
                                        month=self.month,
                                        year=self.year, 
                                        alignment=[])
                    gap_seq_struc.append((gap_rna_seq, gap_structure, prna))
                                                                           
                line1,line2 = None,None
                i = 0
                
        nb_seq = 0
        for (seq, struct, prna) in gap_seq_struc:
            prnas_list.append(prna)
            if not prna.sys_id.startswith("%"):                
                self.prnas_to_add.append(prna)
                nb_seq += 1
            
        align_id = self.id_gen.get_new_alignment_id(self.user_id,
                                                    self.project_id)
        for prna in prnas_list:
            prna.alignment.append(align_id)
            
        a = alignment(align_id, entries, self.run_id,
                      program_name="Carnac + Gardenia", program_version="",
                      day=self.day, month=self.month, year=self.year)

        self.aligns_to_add.append(a)
        return [nb_seq, 1]


    def carnac_predict(self, carnac_result_dir):

        STEM_APPEARS_IN=75.0/100.0
        BASE_PAIRED_THRESHOLD=10.0/100.0

        eqfiles = glob.glob(os.path.join(carnac_result_dir, 'carnac/*.eq'))
        nbfiles = len(eqfiles)

        liststems = []
        listbp = []

        bases = 0.0

        for doteq in eqfiles:
            fdoteq = open(doteq, 'r')

            try:
                linecount = 0
                last_stem = 0

                for line in fdoteq:
                    if(linecount > 0):
                        stem_index = int(re.sub(' [ ]+',
                                                ' ',
                                                line.strip()).split(' ')[2])
                        if stem_index > 0:
                            listbp.append(stem_index)
                            if(last_stem != stem_index):
                                liststems.append(stem_index)
                                last_stem = stem_index
                    linecount += 1

                bases += linecount - 1
            finally:
                fdoteq.close()

        liststems.sort()

        retained_stems = []

        while len(liststems) > 0:
            stem_index = liststems.pop()
            stem_count = 1.0
            if len(liststems) > 0:
                t = liststems.pop()
                while t == stem_index and len(liststems) > 0:
                    stem_count += 1
                    t = liststems.pop()
                if t != stem_index:
                    liststems.append(t)
                else:
                    stem_count += 1

            if stem_count/nbfiles >= STEM_APPEARS_IN:
                retained_stems.append(stem_index)

        paired = 0.0

        for stem_index in retained_stems:
            paired += listbp.count(stem_index)

        return bases > 0 and paired/bases >= BASE_PAIRED_THRESHOLD
