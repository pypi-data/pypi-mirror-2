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
import math
import time

from wrapper import wrapper
import blast_yass_merging as merging

"""
yass output example:

*(8292-8822)(1-529) Ev: 8.45093e-185 s: 531/529 f
* "Sample_sequence_Escherichia_coli_str._K-12_substr._MG1655_4156417:4256417" (100001 bp) / "AJ567607.1/20-548__RF00177;SSU_rRNA_5;" (529 bp)
* score = 2544 : bitscore = 653.10
* mutations per triplet 2, 3, 3 (8.54e-02) | ts : 3 tv : 5 | entropy : 5.82946

        |8300     |8310     |8320     |8330     |8340     |8350     |8360       
GATTGAACGCTGGCGGCAGGCCTAACACATGCAAGTCGAACGGTAACAGGAAGAAGCTTGCTTCTTTGCTGACGAGTGGC
|||||||||||||||||||||||||||||||||||||||||||||||||||||.||||||||.|||:|||||||||||||
GAUUGAACGCUGGCGGCAGGCCUAACACAUGCAAGUCGAACGGUAACAGGAAGCAGCUUGCUGCUUCGCUGACGAGUGGC
         |10       |20       |30       |40       |50       |60       |70        

        |8380     |8390     |8400     |8410     |8420     |8430     |8440       
GGACGGGTGAGTAATGTCTGGGAAACTGCCTGATGGAGGGGGATAACTACTGGAAACGGTAGCTAATACCGCATAACGTC
||||||||||||||||||||||||:|||||||||||||||||||||||||||||||||||||||||||||||||||:|||
GGACGGGUGAGUAAUGUCUGGGAAGCUGCCUGAUGGAGGGGGAUAACUACUGGAAACGGUAGCUAAUACCGCAUAAUGUC
         |90       |100      |110      |120      |130      |140      |150       

[...]

*(49780-50310)(1-529) Ev: 8.45093e-185 s: 531/529 f
* "Sample_sequence_Escherichia_coli_str._K-12_substr._MG1655_4156417:4256417" (100001 bp) / "AJ567607.1/20-548__RF00177;SSU_rRNA_5;" (529 bp)
* score = 2544 : bitscore = 653.10
* mutations per triplet 3, 2, 3 (8.54e-02) | ts : 3 tv : 5 | entropy : 5.82946

|49780    |49790    |49800    |49810    |49820    |49830    |49840    |49850    
GATTGAACGCTGGCGGCAGGCCTAACACATGCAAGTCGAACGGTAACAGGAAGAAGCTTGCTTCTTTGCTGACGAGTGGC
|||||||||||||||||||||||||||||||||||||||||||||||||||||.||||||||.|||:|||||||||||||
GAUUGAACGCUGGCGGCAGGCCUAACACAUGCAAGUCGAACGGUAACAGGAAGCAGCUUGCUGCUUCGCUGACGAGUGGC
         |10       |20       |30       |40       |50       |60       |70        
[...]
"""

SEEDS_RFAM = {8:"@#-#---#@-###,##@#-##@##",
              9:"##@#--##---#-@##,###-#-##-###",
              10:"##@-#-#--#@--####,##@###-#@###"
              }


class yass(wrapper):

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
        t1 =  time.clock()
        result = self.get_temporary_file()
        sequence_file = self.get_sequence_file_path()

        d_list = {}
        fdvalue = open(self.dm.get_cluster_file(self.db), "r")
        for line in fdvalue:
            family = line.split("=")[0].replace(' ', '')
            d = int(line.split("=")[1].replace("\n", "").replace(' ', ''))
            d_list[family] = d
        fdvalue.close()

        if self.opts is None:
            cmd = self.exe_path + ' -o ' + result + ' ' + sequence_file +\
                ' ' + self.db
        else:

            if ("p" not in self.opts or 
                ( "p" in self.opts and self.opts["p"] == "")):
                temp_seq = self.seq.data.replace("N", "")
                fdb = open(self.db, "r")                
                temp_db = 0
                for line in fdb:
                    if not line.startswith(">"):
                        temp_db += len(line.replace("N", ""))
                fdb.close()

                weight = math.log( (len(temp_seq)*temp_db)/1000000)\
                    / math.log(4)
                
                weight = int(weight)
                if weight < 8:
                    weight = 8
                if weight > 10:
                    weight = 10

                self.opts["p"] = SEEDS_RFAM[weight]
                temp_db = None

            # format options line
            options = ''
            gap_done = False

            for opt in self.opts:
                if opt == "E" or opt == "C" or opt == "p":
                    options = options + '-' + opt + ' "' + self.opts[opt] + '" '
                if opt == "e" and self.opts[opt] == "no":
                    options = options + '-e 0 '
                if (opt == "go" or opt == "ge") and not gap_done:
                    go = self.opts["go"]
                    ge = self.opts["ge"]
                    options = options + '-G "' + go + "," + ge + '" '
                    gap_done = True
                if opt == "r":
                    rvalues = {"both":"2", "forward":"0", "reverse":"1"}
                    options = options + " -r " + rvalues[self.opts[opt]] + " "
                if opt == "c":
                    cvalues = {"single":"1", "double":"2"}
                    options = options + " -c " + cvalues[self.opts[opt]] + " "
                    
            cmd = self.exe_path + ' ' + options + '-o ' + result +\
                ' ' + sequence_file + ' ' + self.db        
        
        self.launch(cmd)
        [nb_prediction, nb_alignment] = self.memorize_results(result, d_list)
        t2 = time.clock()
        self.trace_predict_event(cmd, nb_prediction, nb_alignment,
                                 t2 - t1, "yass")
        os.remove(result)
        
    def memorize_results(self, result_path, d_list):
        """
        Parse the result file of yass and create RNAML files
        """

        alignments = {}
        first_line_pattern = '\(([0-9]+)-([0-9]+)\)\(([0-9]+)-([0-9]+)\)' +\
            ' Ev: (.+) s: ([0-9]+)\/([0-9]+) ([rf])$'
        second_line_pattern = '\*[ ]*(.+).*\/[ ]*(.+)[ ]*$'
        second_line_pattern = '.*"(.+)".*\/.*"(.+)".*$'
        ali_pattern = '^[A-Za-z-]+$'

        first_line = re.compile(first_line_pattern)
        second_line = re.compile(second_line_pattern)
        ali = re.compile(ali_pattern)

        first_sequence = True
        file_first_line = True

        database_begin = ""
        database_end = ""
        database_sequence = ""
        database_name = ""
        query_begin = ""
        query_end = ""
        query_sequence = ""
        strand = ""
        evalue = ""

        number_of_stars = 0
        fresult = open(result_path, "r")
        for line in fresult:
            if line.startswith('*'):
                number_of_stars += 1

                # if it is the first line 
                if number_of_stars == 1:
                    if not file_first_line:
                        (a, family)= self.memorize_prediction(query_begin,
                                                              query_end, 
                                                              database_begin,
                                                              database_end, 
                                                              evalue,
                                                              strand, 
                                                              database_name, 
                                                              query_sequence, 
                                                              database_sequence)
                        if a is not None:
                            alignments.setdefault(family, []).append(a)
                    if file_first_line:
                        file_first_line = False

                    query_sequence = ""
                    database_sequence = ""
                    l = first_line.search(line)
                    query_begin = l.group(1)
                    query_end = l.group(2)
                    database_begin = l.group(3)
                    database_end = l.group(4)
                    evalue = l.group(5)
                    strand = l.group(8)
                    if strand == 'f':
                        strand = '+'
                    else:
                        strand = '-'
    
                # if it is the third line 
                if number_of_stars == 2:
                    l = second_line.search(line)
                    database_name = l.group(2)

                # if it is the third line 
                if number_of_stars == 4:
                    number_of_stars = 0

            else:
                if ali.search(line):
                    if first_sequence:
                        query_sequence += line.replace('\n', '')
                        first_sequence = False
                    else:
                        database_sequence += line.replace('\n', '')
                        first_sequence = True
        fresult.close()
        try:
            (a, family) = self.memorize_prediction(query_begin, query_end, 
                                                   database_begin, database_end,
                                                   evalue, strand,
                                                   database_name, 
                                                   query_sequence,
                                                   database_sequence)
            if a is not None:
                alignments.setdefault(family, []).append(a)

        except:
            pass

        db_name = self.dm.get_system_db_name(self.db)            
        for f in alignments:
            alignments[f].sort()
            d = d_list[f]
            (prnas, aligns) = merging.merge(f, alignments[f], d,
                                            db_name, self.user_id,
                                            self.project_id, self.run_id,
                                            self.seq, self.program_name,
                                            self.program_version, self.day, 
                                            self.month, self.year,
                                            self.opts["alignments"])
            self.prnas_to_add.extend(prnas)
            self.aligns_to_add.extend(aligns)
            prnas = None
            aligns = None

        self.add_putative_rnas(self.prnas_to_add)
        self.add_alignments(self.aligns_to_add)

        num_prnas = len(self.prnas_to_add)
        num_aligns = len(self.aligns_to_add)
        
        return [num_prnas, num_aligns]



    def memorize_prediction(self, query_begin, query_end, database_begin, 
                            database_end, evalue, strand, database_name, 
                            query_sequence, database_sequence):
        """
        Create RNAspace objects and write them into RNAML files
        """
        db_name = self.dm.get_system_db_name(self.db)
        family = self.get_family(database_name)
        q_begin = long(query_begin)
        q_end = long(query_end)
        d_begin = long(database_begin)
        d_end = long(database_end)
        database_name = self.dm.get_system_db_sequence_name(database_name)

        if q_begin > q_end:
            temp = q_begin
            q_begin = q_end
            q_end = temp
            
        if d_begin > d_end:
            temp = d_begin
            d_begin = d_end
            d_end = temp

        a = merging.align(q_begin, q_end, d_begin, 
                          d_end, query_sequence, database_sequence, 
                          db_name, database_name, strand, "+", 
                          None, "", family, evalue=evalue)
        return (a, family)
