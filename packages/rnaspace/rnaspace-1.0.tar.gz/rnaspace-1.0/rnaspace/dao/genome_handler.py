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
import glob

from data_handler import data_handler

class genome_handler (data_handler):
    """
    This class gathers all information about genomes.
    """

    def __init__(self):
        data_handler.__init__(self)
        self.genomes_directory = self.config.get_genomes_directory()

    def get_species_names(self, domain):
        """
        Return([string])      the list of species names for a domain

        domain(string)        the domain from which we ask names
        """
        
        # if genome directory is not specified in rnaspace.cfg
        if self.genomes_directory is None:
            return None

        species_list = []

        for d in domain:
            # get path for the selected domain
            domain_dir = os.path.join(self.genomes_directory,
                                      d.capitalize())
            domain_dir = os.path.join(domain_dir, 'current/fasta/')
            # check if this domain is available
            if not os.path.isdir(domain_dir):
                return None
            # we append all species in the species_list list
            for species in os.listdir(domain_dir):
                if os.path.isdir(os.path.join(domain_dir, species)):
                    species_number = len(glob.glob(os.path.join(domain_dir, 
                                                                 species +
                                                                '/*.fna')))
                    species_list.append(species + ' ['+ 
                                        str(species_number)+' sequences]')

        # if no species, then return None
        if species_list == []:
            return None
        species_list.sort()
        return species_list


    def get_species_path(self, species):
        """
        Return(string)     the paths for a species and a domain
        
        species(string)    the species name
        """

        for dir in os.listdir(self.genomes_directory):
            domain_dir = os.path.join(self.genomes_directory, dir)
            if os.path.isdir(domain_dir):
                # get path for the selected species                
                domain_dir = os.path.join(domain_dir, 'current/fasta/')
                species_dir = os.path.join(domain_dir, species.split(' ')[0])
                if os.path.isdir(species_dir):
                    # get all multifasta file in this directory
                    species_list = glob.glob(os.path.join(species_dir, '*.fna'))
                    return species_list

        return None

    def get_system_species_name(self, header):
        """
        Return(string)    the species system name for the specified header

        path(string)      the path of the databases
     
        """
        if header.startswith("gi|"):
            temp = header.split('|')[3]
            return "%" + temp.split('.')[0]
        return "%Unknown"

    def get_system_species_sequence_name(self, header):
        """
        Return(string)    the sequence system name

        seq_name(string)  the sequence name
        """
        if header.startswith("gi|"):
            return "%" + header.split('|')[3]
        return "%Unknown"

    def get_header_species_name(self, header):
        if header.startswith("gi|"):
            try:
                temp = header.split('|')[4]
                return temp
            except:
                return "%Unknown"
        return "%Unknown"
