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
from rnaspace.core.prediction.software_manager import software_manager

class cgview_converter (object):
    """ Class cgview_converter: converts objects to cgview format
    """   
       
    def write(self, obj, seq_lentgh, output):
        """ writes a table of objects into a cgview format file
            prnas(type:[object])    the object table to write down
            seq_lentgh(type:int)    the sequence length
            output(type:string)     path to the folder to store the gff file
        """
        if len(obj) > 0:
            if type(obj[0]) == putative_rna or isinstance(obj[0], putative_rna):
                self.__write_putative_rnas(obj, seq_lentgh, output)
            else: raise TypeError( str(type(obj)) + " is not supported by our cgview converter.")

    def __write_putative_rnas(self, prnas, seq_lentgh, output):
        """ writes a table of putative_rna into a cgview file
            prna(type:[putative_rna])  the putative_rna table to write down
            output(type:string)      path to the folder to store the cgview file
        """
        sm = software_manager() 

        cgview_file = open(output, 'a')
        cgview_file.write("#" + prnas[0].genomic_sequence_id + "\n")
        cgview_file.write("%" + str(seq_lentgh) + "\n")
        cgview_file.write("!strand\tslot\tstart\tstop\ttype\tlabel\tmouseover\thyperlink\n")
        for prna in prnas:
            
            soft_type = sm.get_software_type(prna.program_name)
            
            if prna.strand == "-":
                strand = "reverse"
            else:
                strand = "forward"
            info = "Prediction " + prna.user_id + " [" + str(prna.start_position) + ":" + str(prna.stop_position) + "] predicted by " + prna.program_name

            if soft_type.startswith("known"):
                type = "gene"
                layer = 1
            elif soft_type == "abinitio":
                type = "promoter"
                layer = 2
            elif soft_type == "":
                type = "terminator"
                layer = 3
            else:            
                type = "origin_of_replication" 
                layer = 4
            cgview_file.write(strand + "\t" + str(layer) + "\t" + str(prna.start_position) + "\t" + str(prna.stop_position) + "\t" + type + "\t" + prna.family + "\t" + info + "\t-\n")
        cgview_file.close()
