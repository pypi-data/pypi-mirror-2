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

class apollo_gff_converter (object):
    """ Class apollo_gff_converter: converts objects to Apollo GFF
        This object has to be used as following:
            my_var = gff_converter()
            my_var.read(path/to.gff.gff)
            obj = my_var.get_object()
    """   

    def write(self, obj, output):
        """ writes a table of putative RNAa into a GFF file
            prnas(type:[object])    the object table to write down
            output(type:string)     path to the folder to store the gff file
        """
        if len(obj) > 0:
            if type(obj[0]) == putative_rna or isinstance(obj[0], putative_rna):
                self.__write_putative_rnas(obj, output)
            else: raise TypeError( str(type(obj)) + " is not supported by our RNAML converter.")

    def __write_putative_rnas(self, prnas, output):
        """ writes a table of putative_rna into a gff file
            prna(type:[putative_rna])  the putative_rna table to write down
            output(type:string)      path to the folder to store the gff file
        """
        gff_file = open(output, 'a')
        for prna in prnas:
            if prna.family == "unknown":
                family = "ncRNA"
            else:
                family = prna.family                
            gff_file.write(family + "_"+ str(prna.user_id) + "\tncRNA\tncRNA\t" + str(prna.start_position) + "\t" + str(prna.stop_position) + "\t" + str(prna.score) + "\t" + str(prna.strand) + "\t.\n")
        gff_file.close()

        
