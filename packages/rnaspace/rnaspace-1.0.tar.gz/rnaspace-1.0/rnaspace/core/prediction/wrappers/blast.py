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
import re
import time

from wrapper import wrapper
import blast_yass_merging as merging

"""
blast output example:

>AY838364.1/4-510 RF00177;SSU_rRNA_5;
          Length = 507

 Score =  769 bits (852), Expect = 0.0
 Identities = 482/511 (94%), Gaps = 6/511 (1%)
 Strand = Plus / Plus

                                                                        
Query: 8314 taacacatgcaagtcgaac-ggtaacaggaagaagcttgcttctttgctgacgagtggcg 8372
            ||||||||||||||||| | |||||||   ||| ||||||| ||  | ||||||| ||||
Sbjct: 1    taacacatgcaagtcgagccggtaacacataga-gcttgct-ctcgggtgacgagcggcg 58

                                                                        
Query: 8373 gacgggtgagtaatgtctgggaaactgcctgatggagggggataactactggaaacggta 8432
            ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
Sbjct: 59   gacgggtgagtaatgtctgggaaactgcctgatggagggggataactactggaaacggta 118
[...]

 Score =  769 bits (852), Expect = 0.0
 Identities = 482/511 (94%), Gaps = 6/511 (1%)
 Strand = Plus / Plus

                                                                         
Query: 49802 taacacatgcaagtcgaac-ggtaacaggaagaagcttgcttctttgctgacgagtggcg 49860
             ||||||||||||||||| | |||||||   ||| ||||||| ||  | ||||||| ||||
Sbjct: 1     taacacatgcaagtcgagccggtaacacataga-gcttgct-ctcgggtgacgagcggcg 58

                                                                         
Query: 49861 gacgggtgagtaatgtctgggaaactgcctgatggagggggataactactggaaacggta 49920
             ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
Sbjct: 59    gacgggtgagtaatgtctgggaaactgcctgatggagggggataactactggaaacggta 118

[...]

>EF619951.1/41-571 RF00177;SSU_rRNA_5;
          Length = 531

 Score =  751 bits (832), Expect = 0.0
 Identities = 481/524 (91%)
 Strand = Plus / Plus

                                                                        
Query: 8299 cgctggcggcaggcctaacacatgcaagtcgaacggtaacaggaagaagcttgcttcttt 8358
            |||||| ||| || |  ||  ||||||||||||||| ||||||||| |||||||| ||||
Sbjct: 8    cgctggtggctggacagacgtatgcaagtcgaacgggaacaggaagcagcttgctgcttt 67
[...]
"""

class blast(wrapper):

    def __init__(self, opts, seq, user_id, project_id, run_id, p,
                 stderr, stdout, program_name, type, thread_name, version, exe):
        wrapper.__init__(self, opts, seq, user_id, project_id, run_id, p,
                         stderr, stdout, program_name, type, thread_name, 
                         version, exe)
        self.alignments_to_add = []
        self.prnas_to_add = []
        self.alignments = {}

    def run(self):
        try:
            self.__run()
        except Exception:
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
        
        t1 =  time.clock()

        d_list = {}
        fdvalue = open(self.dm.get_cluster_file(self.db), "r")
        for line in fdvalue:
            family = line.split("=")[0].replace(' ', '')
            d = int(line.split("=")[1].replace("\n", "").replace(' ', ''))
            d_list[family] = d
        fdvalue.close()
        
        query_strands = {'both':'3', 'forward':'1', 'reverse':'2'}
        # construct options line
        options = '-b 40000000 '
        if self.opts is not None:
            for opt in self.opts:
                if self.opts[opt] != '' and opt != 'alignments':
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

        result = self.get_temporary_file()
        sequence_file = self.get_sequence_file_path()

        cmd = self.exe_path + ' -p blastn ' + options + '-o ' + result +\
            ' -i ' + sequence_file + ' -d ' + self.db 

        self.launch(cmd)
        
        [nb_prediction, nb_alignment] = self.memorize_results(result, d_list)
        t2 = time.clock()
        self.trace_predict_event(cmd, nb_prediction, nb_alignment,
                                 t2 - t1, "blast")
        os.remove(result)
        
    def memorize_results(self, result_path, d_list):
        """
        Parse blast result file and write RNAML files.        
        """

        alignments = {}
        
        finput = open(result_path, "r")
                
        query_ali_pattern = '^Query: ([0-9]+) +([A-Za-z-]+) +([0-9]+)$'
        database_ali_pattern = '^Sbjct: ([0-9]+) +([A-Za-z-]+) +([0-9]+)$'
        score_pattern = ' Score =[ ]+([0-9.]+).*, Expect = ([.0-9\-e]+)'
        strand_pattern = ' Strand = ([a-zA-Z]+) / ([a-zA-Z]+)'

        score_line = re.compile(score_pattern)
        strand_line = re.compile(strand_pattern)
        query_ali = re.compile(query_ali_pattern)
        database_ali = re.compile(database_ali_pattern)

        file_first_sequence = True
        new_query_sequence = False
        new_alignment = False
        
        database_begin = 0
        database_end = 0
        database_sequence = ""
        database_strand = ""
        database_name= ""
        query_begin = 0
        query_end = 0
        query_sequence = ""
        query_strand = ""
        score = ""
        expect = ""
        begin_name = 0
        nohits = False
        
        result = []
        for (i, line) in enumerate(finput):
            result.append(line)
            if line.startswith(' ***** No hits found ******'):
                nohits = True
                break
            if line.startswith('>'):

                if not file_first_sequence:
                    (a, family) = self.memorize_prediction(database_name, 
                                                           score, expect, 
                                                           query_strand,
                                                           database_strand, 
                                                           query_begin,
                                                           query_sequence, 
                                                           query_end,
                                                           database_begin, 
                                                           database_sequence,
                                                           database_end)
                    if a is not None:
                        alignments.setdefault(family, []).append(a)
                else:
                    file_first_sequence = False

                new_query_sequence = True            
                query_sequence = ""
                database_name = line.replace("\n", "")
                begin_name = i
                database_sequence = ""

            if line.find("Length = ") != -1:
                for k in range(begin_name+1, i):
                    database_name += result[k].replace("\n", "").strip()

            if line.startswith(' Score'):
                if not new_query_sequence:
                    (a, family) = self.memorize_prediction(database_name, 
                                                           score, expect, 
                                                           query_strand,
                                                           database_strand, 
                                                           query_begin,
                                                           query_sequence, 
                                                           query_end,
                                                           database_begin, 
                                                           database_sequence,
                                                           database_end)
                    alignments.setdefault(family, []).append(a)
                else:
                    new_query_sequence = False

                query_sequence = ""
                database_sequence = ""

                new_alignment = True
                l = score_line.search(line)
                score = l.group(1)
                expect = l.group(2)                                
                if expect.startswith("e"):
                    expect = "1" + expect

            if line.startswith(' Strand'):
                l = strand_line.search(line)
                query_strand = "-" 
                if l.group(1) == "Plus":
                    query_strand = "+"                    
                database_strand = "-"
                if l.group(2) == "Plus":
                    database_strand = "+"

            if line.startswith('Query:'):
                l = query_ali.search(line)
                if new_alignment:
                    query_begin = long(l.group(1))
                query_end = long(l.group(3))
                query_sequence += l.group(2)            
                        
            if line.startswith('Sbjct:'):
                l = database_ali.search(line)
                if new_alignment:
                    database_begin = long(l.group(1))
                    new_alignment = False
                database_end = long(l.group(3))
                database_sequence += l.group(2)            

        try:
            if not nohits:
                (a, family) = self.memorize_prediction(database_name, score,
                                                       expect, query_strand,
                                                       database_strand,
                                                       query_begin,
                                                       query_sequence,
                                                       query_end,
                                                       database_begin, 
                                                       database_sequence,
                                                       database_end)
                if a is not None:
                    alignments.setdefault(family, []).append(a)
        except:
            pass

        db_name = self.dm.get_system_db_name(self.db)
        for f in alignments:
            alignments[f].sort()
            d = d_list[f]
            (prnas, aligns) = merging.merge(f, alignments[f], d, db_name, 
                                            self.user_id, self.project_id, 
                                            self.run_id, self.seq,
                                            self.program_name,
                                            self.program_version, self.day, 
                                            self.month, self.year,
                                            self.opts["alignments"])
            self.prnas_to_add.extend(prnas)
            self.alignments_to_add.extend(aligns)

        self.add_putative_rnas(self.prnas_to_add)
        self.add_alignments(self.alignments_to_add)        
        finput.close()
        del alignments
        return [len(self.prnas_to_add), len(self.alignments_to_add)]

    def memorize_prediction(self, database_name, score, expect, 
                            query_strand, database_strand, query_begin, 
                            query_sequence, query_end, database_begin, 
                            database_sequence, database_end):

        db_name = self.dm.get_system_db_name(self.db)        
        database_sys_name = self.dm.get_system_db_sequence_name(database_name)
        family = self.get_family(database_name)
        q_begin = long(query_begin)
        q_end = long(query_end)
        d_begin = long(database_begin)
        d_end = long(database_end)
        if q_begin > q_end:
            q_end = long(query_begin)
            q_begin = long(query_end)
            
        if d_begin > d_end:
            d_end = long(database_begin)
            d_begin = long(database_end)

        a = merging.align(q_begin, q_end, d_begin, d_end, query_sequence,
                          database_sequence,
                          db_name, database_sys_name, query_strand, 
                          database_strand, None, "", family, 
                          evalue=expect)
        return (a, family)
