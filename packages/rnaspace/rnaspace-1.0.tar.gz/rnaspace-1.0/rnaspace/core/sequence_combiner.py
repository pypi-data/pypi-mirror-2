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

from putative_rna import putative_rna
from id_tools import id_tools
import data_manager

SHIFT = 10

class sequence_combiner (object):
    """
    Class sequence_combiner: combine sequence
    """
    
    combine_type = {"basic_combine" : ""}

    def __init__(self):
        self.data_manager = data_manager.data_manager()

    def run (self, user_id, project_id, prnas, combine_type, **params):
        """ 
        Combine all putative rnas given 
        user_id(type:string)      user id of the connected user
        project_id(type:string)   the project the user is working on
        prnas([putative_rnas])    the prnas to combine
        combine_type(string)      the combiner algorithm to use
        **params({string:string}) combiner parameters
        """  
        if combine_type in self.combine_type:
            if combine_type == "basic_combine":
                return self.__run_basic_combine(user_id, project_id, prnas) 

    def __get_complement(self, base):
        """ 
        Return the complement base
        base(string)     the base to complement
        """
        cbase_table = {
            'A': 'T',
            'a': 't',
            'T': 'A',
            't': 'a',
            'C': 'G',
            'c': 'g',
            'G': 'C',
            'g': 'c',
            'U': 'A',
            'u': 'a',
            'N': 'N',
            'n': 'n'}
        return cbase_table[base]
 
    def __get_reverse_complement(self, seq):
        """ Return the reverse complement sequence
        seq(string)     the sequence to reverse and complement
        """
        rc_seq = ""
        for base in reversed(seq):
            rc_seq += self.__get_complement(base)
        return rc_seq

    
    def __change_alignment_id(self, user_id, project_id, prna, new_id):
        if prna.alignment is not None:
            align_list = []
            align_ids = []
            for align_id in prna.alignment:
                align = self.data_manager.get_alignment(user_id, project_id,
                                                        align_id)
                for entry in align.rna_list:
                    if entry.rna_id == prna.sys_id:
                        if entry.rna_id == entry.user_id:
                            entry.user_id = new_id
                        entry.rna_id = new_id

                align_list.append(align)
                align_ids.append(align_id)

            if len(align_list) > 0:        
                self.data_manager.add_alignments(user_id, project_id, 
                                                 align_list)
                return align_ids
            
        return None

    def __merge_prnas(self, user_id, project_id, prnaA, prnaB):
        """
        Merge two prnas and return the new one
        """

        sequence_id = prnaA.genomic_sequence_id
        user_seq = self.data_manager.get_sequence(user_id, sequence_id,
                                                  project_id)
        
        # get begin and end positions of the new prnas
        begin = min(prnaA.start_position, prnaB.start_position)
        end = max(prnaA.stop_position, prnaB.stop_position)

        # nice program name: combine:soft1/soft2/soft3...
        if prnaA.program_name != prnaB.program_name:
            psA = prnaA.program_name.split(":")
            psB = prnaB.program_name.split(":")
            if len(psA) > 1:
                programsA = psA[1].split("+")
            else:
                programsA = psA

            if len(psB) > 1:
                programsB = psB[1].split("+")
            else:
                programsB = psB

            for program in programsA:
                if program not in programsB and program != "":
                    programsB.append(program)

            programsB.sort()
            program_name = "combine:" + "+".join(p for p in programsB)
        else:
            ps = prnaA.program_name.split(":")
            if len(ps) > 1:
                programs = ps[1].split("+")
                programs.sort()
                program_name = "combine:" + "+".join(p for p in programs)
            else:
                program_name = "combine:" + prnaA.program_name
                
        strand = prnaA.strand

        if strand == "-":
            sequence = self.__get_reverse_complement(user_seq.data[begin:end])
        else:
            sequence = user_seq.data[begin:end]

        align_list = self.__change_alignment_id(user_id, project_id, 
                                                prnaB, prnaA.sys_id)
                
        new_align = prnaA.alignment
        if new_align is not None and align_list is not None:
            new_align.extend(align_list)
        else:
            if align_list is not None:
                new_align = align_list

        # create the new prna
        prna = putative_rna(prnaA.sys_id, prnaA.genomic_sequence_id, 
                            begin, end, prnaA.run, prnaA.sys_id, 
                            sequence, prnaA.family, strand, 
                            prnaA.domain, prnaA.species, prnaA.strain, 
                            prnaA.replicon, [], 0.0, program_name, 
                            prnaA.program_version,
                            str(time.localtime()[2]),
                            str(time.localtime()[1]), 
                            str(time.localtime()[0]), new_align)
        
        return prna

    def __basic_combine(self, prnas, user_id, project_id):

        # if the family is Unknown, do not combine prnas
        if prnas[0].family == "Unknown" or prnas[0].family == "unknown":
            return prnas

        # sort prnas by their begin position
        prnas.sort(cmp=lambda x,y: cmp(x.start_position, y.start_position))

        # initialisation
        id_gen = id_tools()
        prna_id = id_gen.get_new_putativerna_id(user_id, project_id,
                                                prnas[0].genomic_sequence_id)
        prna = prnas[0]
        align_list = self.__change_alignment_id(user_id, project_id,
                                                prna, prna_id)

        newprna = putative_rna(prna_id, prna.genomic_sequence_id, 
                               prna.start_position, prna.stop_position, 
                               prna.run, prna_id, prna.sequence, 
                               prna.family, prna.strand, prna.domain, 
                               prna.species, prna.strain,
                               prna.replicon, prna.structure, 
                               prna.score, prna.program_name, 
                               prna.program_version,
                               str(time.localtime()[2]),
                               str(time.localtime()[1]), 
                               str(time.localtime()[0]), align_list)
        merged = [newprna]
        k = 0
        for prna in prnas[1:]:
            current_begin = merged[k].start_position
            current_end = merged[k].stop_position
            if( (current_begin - SHIFT <= prna.start_position and
                 prna.stop_position <= current_end + SHIFT) or
                (prna.start_position <= current_begin and
                 current_end <= prna.stop_position) ):

                # merge the current prna with the previous one
                merged[k] = self.__merge_prnas(user_id, project_id, merged[k],
                                               prna)
            else:
                # create a new prediction
                id_gen = id_tools()
                prna_id = id_gen.get_new_putativerna_id(user_id, project_id,
                                                        prna.genomic_sequence_id)
                align_list = self.__change_alignment_id(user_id, project_id,
                                                        prna, prna_id)

                newprna = putative_rna(prna_id, prna.genomic_sequence_id, 
                                       prna.start_position, prna.stop_position, 
                                       prna.run, prna_id, prna.sequence, 
                                       prna.family, prna.strand, prna.domain, 
                                       prna.species, prna.strain,
                                       prna.replicon, prna.structure, 
                                       prna.score, prna.program_name, 
                                       prna.program_version,
                                       str(time.localtime()[2]),
                                       str(time.localtime()[1]), 
                                       str(time.localtime()[0]), 
                                       align_list)
                merged.append(newprna)
                k = k + 1
        
        return merged

    def __run_basic_combine(self, user_id, project_id, prnas):        
        """
        combine prnas and return the new ones

        Return([putative_rna])

        user_id(string):       the current user id
        project_id(string):    the current project id
        prnas([putative_rna]): the prnas to merge
        """


        rnas_per_family = {}
        new_prnas = []

        # regroup prnas per input sequence, family and strand
        for prna in prnas:
            gs_id = prna.genomic_sequence_id            
            strand = prna.strand
            family = prna.family.lower()
            
            rnas_per_family.setdefault(gs_id, {})
            rnas_per_family[gs_id].setdefault(family, {})
            rnas_per_family[gs_id][family].setdefault(strand, [])
            rnas_per_family[gs_id][family][strand].append(prna)

        # combine prnas for each family
        for gs_id in rnas_per_family:
            for family in rnas_per_family[gs_id]:
                for strand in rnas_per_family[gs_id][family]:
                    combined = self.__basic_combine(rnas_per_family[gs_id][family][strand], user_id, project_id)
                    new_prnas.extend(combined)

        return new_prnas
