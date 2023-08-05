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

class alignment_entry:
            
    def __init__(self, rna_id, sequence, start, stop, genomic_sequence_id,
                 structure=None, replicon="", domain="", species="",
                 strain="",strand="", user_id="", family="unknown"):

        self.rna_id = rna_id
        self.sequence = sequence
        self.structure = structure
        self.start = long(start)
        self.stop = long(stop)
        if self.start > self.stop:
            self.size = self.start - self.stop + 1
        else:
            self.size = self.stop - self.start + 1
        self.genomic_sequence_id = genomic_sequence_id
        self.replicon = replicon
        self.domain = domain
        self.species = species
        self.strain = strain
        self.strand=strand
        self.family = family
        if user_id == "":
            self.user_id = rna_id
        else:
            self.user_id = user_id

class alignment:

    def __init__(self, id, rna_list, run_id, consensus=None, program_name="",
                 program_version="", day="", month="", year="", score="", 
                 evalue="", pvalue=""):
        
        """
        id(string)                       system id, unique
        rna_list([])                     list of rna involved in the alignment
        consensus(putative_rna)          consensus
        run_id(string)                   id of the run
        program_name(string)             name of the soft that did the align.
        program_version(string)          version of the soft
        day(string)                      day
        month(string)                    month
        year(string)                     year
        """
        
        self.id = id
        self.run_id = run_id

        self.rna_list = rna_list
       
        self.consensus = consensus

        self.program_name = program_name
        self.program_version = program_version

        self.day = day
        self.month = month
        self.year = year
                
        self.score = score
        self.evalue = evalue
        self.pvalue = pvalue
