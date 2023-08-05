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



class sequence (object):
    """
    Class sequence: gathers all information on a sequence
    """   
    
    def __init__(self, id, data, domain = "unknown", species = "unknown",
                 replicon = "unknown", strain="unknown"):
        """ 
        Build a sequence object defined by 

        id(type:string)        has to be unique 
        data(type:string)      ACTG sequence             
        domain(type:string)    domain name                               
        species(type:string)   species name                              
        replicon(type:string)  replicon value (chromosom, plasmid or 
                               special name: chV)   
        """
        self.id = id
        self.domain = domain
        self.species = species
        self.replicon = replicon
        self.strain = strain
        self.data = data

    def __len__(self):
        return len(self.data)

    def is_bacteria(self):
        if self.domain == 'bacteria':
            return True
        else:
            return False

    def is_eukaryote(self):
        return self.domain == 'eukaryote'

    def is_archaea(self):
        if self.domain == 'archaea':
            return True
        else:
            return False
