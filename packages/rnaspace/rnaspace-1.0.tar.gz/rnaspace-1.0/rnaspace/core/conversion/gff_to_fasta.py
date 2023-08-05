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


class gff_to_fasta:
    
    def convert(self, gff, fasta):

        fgff = open(gff, 'r')
        ffasta = open(fasta, 'w')
        
        write_test = False
        for line in fgff.readlines():
            if line.startswith('##FASTA'):
                write_test = True
            elif write_test:
                if line.startswith('>'):
                    #ffasta.write(line.split('\t')[0] + '\n')
                    ffasta.write(line)
                else:
                    l = line.lower()                    
                    ffasta.write(l)

        fgff.close()
        ffasta.close()
