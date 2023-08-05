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



class secondary_structure (object):
    """ 
    Class structure: gathers all information on a rna structure
    """
    
    def __init__(self, format = "", structure = "", predictor = "", 
                 free_energy = 0.0):
        """ 
        Build a secondary_structure object defined by 

        format(type:string)       the format of the secondary structure
        structure(type:string)    the parenthesis structure                  
        predictor(type:string)    predictor name that had predicted the sequence
        free_energy(type:float)   the structure free energy              
        """
        self.structure = structure
        self.predictor = predictor   
        self.free_energy = free_energy
        self.format = format

    def converts_to_brackets(self):
        """ Converts brackets annotation: <> to ()
        """
        self.structure = self.structure.replace("<","(")
        self.structure = self.structure.replace(">",")")
