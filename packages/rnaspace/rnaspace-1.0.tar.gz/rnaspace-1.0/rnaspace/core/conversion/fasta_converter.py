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


from rnaspace.core.putative_rna import putative_rna

class fasta_converter (object):
    """ Class fasta_converter: converts objects to fasta or read fasta to objects
        This object has to be used as following:
            my_var = fasta_converter()
            my_var.read(path/to.fasta.fna)
            obj = my_var.get_object()
    """   

    def write(self, obj, output):
        """ writes a table of object into an fasta file
            prnas(type:[object])    the object table to write down
            output(type:string)     path to the folder to store the rnaml file
        """
        if len(obj) > 0:
            if type(obj[0]) == putative_rna or isinstance(obj[0], putative_rna):
                self.__write_putative_rnas(obj, output)
            else: raise TypeError( str(type(obj)) + " is not supported by our rnaml converter.")

    def __write_putative_rnas(self, prnas, output):
        """ writes a table of putative_rna into an fasta file
            prna(type:[putative_rna])  the putative_rna table to write down
            output(type:string)      path to the folder to store the rnaml file
        """
        fasta_file = open(output, 'a')
        for prna in prnas:
            header = ">"+prna.user_id+"|"+prna.family
            if prna.domain != "":
                header += "|" + prna.domain
            if prna.species != "":
                header += "|" + prna.species
            if prna.strain != "":
                header += "|" + prna.strain
            if prna.replicon != "":
                header += "|" + prna.replicon
            header += "|" + prna.strand + "|" + str(prna.start_position) + "|" + str(prna.stop_position) + "\n"
            fasta_file.write(header)
            fasta_file.write(prna.sequence + "\n")
        fasta_file.close()
        
        
