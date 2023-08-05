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


import re

class putative_rna (object):
    """
    Class putative_rna: gathers all information on a putative rna
    """   
    
    validity_regexp = "^[0-9A-Za-z_.,/')(-]+$"
    
    def __init__(self, id, genomic_sequence_id, start_position, stop_position,
                 run, user_id = "", sequence = "", family = "unknown",
                 strand = "", domain = "", species = "", strain = "", replicon = "",
                 structure = [], score = 0.0, 
                 program_name = "", program_version = "", day = "", 
                 month = "", year = "", alignment=None):
        """ 
        Build a putative rna object defined by:    

        sys_id(type:string)                    system id, has to be unique      

        user_id(type:string)                   user id, has to be unique 

        genomic_sequence_id(type:string)       the genomic sequence id from
                                               which  the putative rna has 
                                               been deteced          

        family(type:string)                    family name, name of the
                                               Rfam or new      

        start_position(type:integer)           genomic begining position
                                               on the replicon  
        stop_position(type:integer)            genomic ending position on 
                                               the replicon         

        size(type:integer)                     size of the putative rna 
        strand(type:string)                    strand value [+, -] 
        sequence(type:string)                  sequence of the putative rna

        domain(type:string)                    domain name 
        species(type:string)                   species name 
        replicon(type:string)                  replicon value (chromosom, 
                                               plasmid or  special name: chV) 

        structure(type:[secondary_structure])  table of secondary structure

        score(type:float)                      score of the prediction      

        run(type:string)                       run number by which the 
                                               putative rna has been predicted

        program_name(type:string)              name of the program that has 
                                               predicted the putative rna
        program_version(type:string)           version of the program that has 
                                               predicted the putative rna 

        day(type:string)                       day of the prediction
        month(type:string)                     month of the prediction
        year(type:string)                      year of the prediction

        alignment(type:[string])               ids of the alignments in which
                                               the prna is involved
        """
        # Required attributs
        self.sys_id = id
        self.genomic_sequence_id = genomic_sequence_id
        self.start_position = long(start_position)
        self.stop_position = long(stop_position)
        self.run = run
        
        # Optional attributs
        self.sequence = sequence
        if self.is_valid(family):
            self.family = family
        else :
            self.family = "unknown"
            
        if strand == "+" or strand == "-" or strand == ".":
            self.strand = strand
        else:
            if self.start_position <= self.stop_position:
                self.strand = "."
            else:
                self.strand = "-"
            
        if self.start_position > self.stop_position:
            self.start_position, self.stop_position = self.stop_position, self.start_position 

        if self.is_valid(domain):
            self.domain = domain
        else :
            self.domain = "unknown"

        if self.is_valid(species):
            self.species = species
        else :
            self.species = "unknown"
        
        if self.is_valid(strain):
            self.strain = strain
        else :
            self.strain = "unknown"

        if self.is_valid(replicon):
            self.replicon = replicon
        else :
            self.replicon = "unknown"

        self.structure = structure
        self.score = float(score)
        self.program_name = program_name
        self.program_version = program_version
        self.day = day
        self.month = month
        self.year = year   
        if user_id == "":
            self.user_id = id
        else: 
            self.user_id = user_id
        self.alignment = []
        if alignment != None:
            self.alignment.extend(alignment)
        
        # Computed attributs
        if self.start_position < self.stop_position:
            self.size = long(self.stop_position) - self.start_position + 1
        else:
            self.size = self.start_position - self.stop_position + 1


    def get_x(self, x):
        """
        Return the value of the putative_rna attribute defined by x. 
        If a wrong attribute is given, an empty string is returned
        """
        try:
            attr_value = getattr(self, x)
        except AttributeError:
            return ""
        return attr_value

    def set_x(self, x, value):
        """
        Set the value of the putative_rna attribute defined by x. 
        If a wrong attribute is given, nothing is done
        """
        if x in self.__dict__:
            try:
                setattr(self, x, value)
            except AttributeError:
                pass

    def print_putative_rna(self):
        """
        debug function: print a putative_rna object
        """
        for i in self.__dict__:
            if i != "structure":
                print i + " : " + str(self.__getattribute__(i))
        for i in self.structure:
            print "struct : " + str(i.structure) + " " + \
                str(i.predictor) + " " + str(i.free_energy)
    
    @staticmethod
    def is_valid (value):
        """
        return True if the field match the regular expression, false otherwise
        """
        return re.search(putative_rna.validity_regexp, value)

    def __eq__(self, prnaB):
        """
        Return(type:Boolean)      return True if the 2 rnas are egals
                                  False otherwise 
        """
        return (self.start_position == prnaB.start_position and
                self.stop_position == prnaB.stop_position and
                self.sequence == prnaB.sequence and
                self.genomic_sequence_id == prnaB.genomic_sequence_id)

