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
import re

import rnaspace.core.common as common
from rnaspace.core.sequence import sequence
from data_handler import data_handler
from user_handler import user_handler
from rnaspace.core.exceptions import disk_error, project_space_error, user_space_error

class sequence_handler(data_handler):
    """ 
    Class sequence_handler: this data handler control all the data dealing with
    a sequence
    """

    def __init__(self):
        data_handler.__init__(self)
        self.user_handler = user_handler()

    def get_sequence(self, user_id, sequence_id, project_id = "0"):
        """
        Return(sequence)          the sequence specified by its id 
        for a specified user and project

        user_id(type:string)      user id of the connected user
        sequence_id(type:string)  the squence id required
        project_id(type:string)   project id the user is working on
        """
        path = self.config.get_sequence_directory(user_id, project_id)
        if path != None:
            file = os.path.join(path, sequence_id + ".fna")
            infos_path = os.path.join(path, sequence_id + ".txt")
            if os.path.isfile(file):
                data = ""
                for ligne in open(file):
                    if (not re.search(">.*", ligne)): # This is the header
                        data += ligne
                data = data.replace("\n","")
                
                infos_file = open(infos_path, 'r')
                infos = infos_file.read().split('\n')
                infos_dict = {}
                for line in infos:
                    info = line.split('=')
                    infos_dict[info[0]] = info[1]

                infos_file.close()

                seq = sequence(sequence_id, data, 
                               domain=infos_dict['domain'],
                               replicon=infos_dict['replicon'],
                               species=infos_dict['species'], 
                               strain=infos_dict['strain'])
                return seq
            else:
                raise IOError("The sequence " + sequence_id + " doesn't exist.")

    def get_sequences_id(self, user_id, project_id):
        """ 
        Return([string])          a table of all sequences id linked 
                                  to the project
        
        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        """
        ids = []
        path = self.config.get_sequence_directory(user_id, project_id)
        if path != None:
            for seq in os.listdir(path):
                # if it's a fasta file
                if (re.search(".*.fna", seq)):
                    tab = re.search("(.*).fna", seq)
                    ids.append(tab.group(1))
        return ids

    def add_sequence(self, user_id, project_id, seq):
        """
        Raise disk_error if no more space available
        Raise KeyEroor if sequence id already exists
        
        Add a sequence to the user

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        seq(type:sequence)        the sequence to add
        """
        max_user_size = common.get_nb_octet(self.config.get("storage", "user_size_limitation"))
        max_project_size = common.get_nb_octet(self.config.get("storage", "project_size_limitation"))
        user_space = self.user_handler.get_user_used_space(user_id)
        project_space = self.user_handler.get_project_used_space(user_id,
                                                                 project_id)

        if user_space > max_user_size: 
            raise user_space_error(user_id, project_id,
                                   disk_error.sequence_message)
        
        if project_space > max_project_size:
            raise project_space_error(user_id, project_id,
                                      disk_error.sequence_message)
        
        if not self.sequence_exists(user_id, project_id, seq.id):
            path = self.config.get_sequence_directory(user_id, project_id)
            fasta_path = os.path.join(path, seq.id + '.fna')
            info_path = os.path.join(path, seq.id + '.txt')
    
            fasta_file = open(fasta_path, 'w')
            fasta_file.write(seq.data)
            fasta_file.close()
    
            info_file = open(info_path, 'w')
            info_file.write('domain=' + seq.domain + '\n')
            info_file.write('species=' + seq.species + '\n')
            info_file.write('strain=' + seq.strain + '\n')
            info_file.write('replicon=' + seq.replicon)
            info_file.close()
            size = self.get_disk_size(fasta_path)

            self.user_handler.update_project_used_space(user_id, project_id,
                                                        size)
            self.user_handler.update_project_sequences_used_space(user_id,
                                                                  project_id,
                                                                  size)
        else:
            raise KeyError, "Sequence id already exists."

    def sequence_exists(self, user_id, project_id, seq_id):
        """
        Check if a sequence already exists

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        seq_id(type:string)       the sequence id to check
        """
        ids = self.get_sequences_id(user_id, project_id)
        return seq_id in ids

    def get_sequence_file(self, user_id, project_id, seq_id):
        """
        Return(type:string)   the content of the sequence file defined by seq_id

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        seq_id(type:string)       the sequence id
        """
        fasta_path = self.config.get_sequence_directory(user_id, project_id)
        fasta_file = open(os.path.join(fasta_path, seq_id + '.fna'), 'r')
        seq = fasta_file.read()
        fasta_file.close()

        return seq
    
    def get_sequence_file_path(self, user_id, project_id, seq_id):
        """
        Return(type:string)   the path of the sequence file defined by seq_id

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        seq_id(type:string)       the sequence id
        """
        path = self.config.get_sequence_directory(user_id, project_id)
        path = os.path.join(path, seq_id + '.fna')
        return path

    def get_sequence_directory(self, user_id, project_id):
        """
        Return(type:string)       return the sequence directory

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        """
        return self.config.get_sequence_directory(user_id, project_id)


    def get_sequence_header(self, user_id, project_id, seq_id):
        """
        Return(type:string)       the header of a sequence

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        seq_id(type:string)       the sequence id
        """
        path = self.config.get_sequence_directory(user_id, project_id)
        path = os.path.join(path, seq_id + '.fna')
        fpath = open(path, 'r')
        seq = fpath.read()
        fpath.close()
        seq = seq.split('\n')
        return seq[0][1:]
