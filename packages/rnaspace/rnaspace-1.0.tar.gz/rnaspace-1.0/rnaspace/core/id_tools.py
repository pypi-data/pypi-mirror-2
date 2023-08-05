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
import threading
import uuid

import data_manager

class id_tools:

    # lock objects to protect threads shared files 
    lock_run = threading.Lock()
    lock_sequence = threading.Lock()
    lock_project = threading.Lock()
    lock_prna = threading.Lock()
    lock_alignment = threading.Lock()


    def __init__(self):
        self.data_m = data_manager.data_manager()

    def get_nb_string(self, last, length=6):  
        """Return a string of 6 caracters."""
        zeros = ""
        new = last + 1
        s_new = str(new)
        len_s_new = len(s_new)
        for i in range(length - len_s_new):
            zeros += "0";
        s_new = zeros + s_new
        return s_new

    def get_new_project_id(self, user_id):
        """
        Create a new project id.
        
        Return(type:string)     the new id

        user_id(string)         id of the connected user
        """
        id_tools.lock_project.acquire()
        try:
            last = self.data_m.get_user_last_project_id(user_id)            
            temp_id = self.get_nb_string(last)
            self.data_m.update_user_last_project_id(user_id, temp_id)
        finally:
            id_tools.lock_project.release()

        return temp_id + uuid.uuid4().hex[:9]

    def get_new_run_id(self, user_id, project_id):
        """
        Create a new run id. The last id is saved in
        user directory under the name "lastrunid"

        Return(type:string)     the new id

        user_id(string)         id of the connected user
        project_id(string)      id of the project
        """
        
        id_tools.lock_run.acquire()
        try:
            last = self.data_m.get_last_run_id(user_id, project_id)
            temp_id = self.get_nb_string(last,2)
            self.data_m.update_last_run_id(user_id, project_id, temp_id)
        finally:
            id_tools.lock_run.release()

        return "r" + temp_id

    def get_new_sequence_id(self, user_id, project_id):
        """
        Create a new run id. The last id is saved in
        user directory under the name "lastseqid"

        Return(type:string)     the new id

        user_id(string)         id of the connected user
        project_id(string)      id of the project
        """

        id_tools.lock_sequence.acquire()
        try:
            seq_dir = self.data_m.get_sequence_directory(user_id, project_id)
            lastseq_path = os.path.join(seq_dir, 'lastseqid')
            if os.path.isfile(lastseq_path):
                flast = open(lastseq_path, 'r')
                last = int(flast.read())
                flast.close()
            else:
                last = 0
        
            temp_id = self.get_nb_string(last)
            flast = open(lastseq_path, 'w')
            flast.write(temp_id)
            flast.close()
        finally:
            id_tools.lock_sequence.release()

        return "seq_" + temp_id

    def get_current_sequence_id(self, user_id, project_id):
        """
        Return(type:string)     the current id

        user_id(string)         id of the connected user
        project_id(string)      id of the project
        """
        id_tools.lock_sequence.acquire()
        try:
            try:
                seq_dir = self.data_m.get_sequence_directory(user_id, project_id)
                lastseq_path = os.path.join(seq_dir, 'lastseqid')
                if os.path.isfile(lastseq_path):
                    flast = open(lastseq_path, 'r')
                    last = int(flast.read())
                    flast.close()
                else:
                    last = 0
            except:
                last = 0
            temp_id = self.get_nb_string(last)

        finally:
            id_tools.lock_sequence.release()
        return "seq_" + temp_id

    def get_new_putativerna_id(self, user_id, project_id, seq_id):
        """
        Create a new putative rna id. The last id is saved in
        user directory under the name "lastprnaid"

        Return(type:string)     the new id

        user_id(string)         id of the connected user
        project_id(string)      id of the project
        """

        id_tools.lock_prna.acquire()
        try:
            prna_dir = self.data_m.get_putative_rna_directory(user_id,
                                                              project_id)
            lastprna_path = os.path.join(prna_dir, 'lastprnaid')        
            if os.path.isfile(lastprna_path):
                flast = open(lastprna_path, 'r')
                last = int(flast.read())
                flast.close()               
            else:
                last = 0        
            temp_id = self.get_nb_string(last)        
            flast = open(lastprna_path, 'w')
            flast.write(temp_id)
            flast.close()            
        finally:
            id_tools.lock_prna.release()

        return temp_id

    def get_current_putative_rna_id(self, user_id, project_id, seq_id):
        """
        Return the current rna_id
        user directory under the name "lastprnaid"
        Return(type:string)     the current id
        user_id(string)         id of the connected user
        project_id(string)      id of the project
        """

        id_tools.lock_prna.acquire()
        try:
            prna_dir = self.data_m.get_putative_rna_directory(user_id,
                                                              project_id)
            lastprna_path = os.path.join(prna_dir, 'lastprnaid')        
            if os.path.isfile(lastprna_path):
                flast = open(lastprna_path, 'r')
                last = int(flast.read())
                flast.close()               
            else:
                last = 0        
            temp_id = self.get_nb_string(last)                 
        finally:
            id_tools.lock_prna.release()
        return temp_id

    def get_new_alignment_id(self, user_id, project_id):
        """
        Create a new alignment id. The last id is saved in
        user directory under the name "lastalignid"

        Return(type:string)     the new id

        user_id(string)         id of the connected user
        project_id(string)      id of the project
        """

        id_tools.lock_alignment.acquire()
        try:
            align_dir = self.data_m.get_alignment_directory(user_id, project_id)
            lastalign_path = os.path.join(align_dir, 'lastalignid')
            if os.path.isfile(lastalign_path):
                flast = open(lastalign_path, 'r')
                last = int(flast.read())
                flast.close()
            else:
                last = 0
        
            temp_id = self.get_nb_string(last)
            flast = open(lastalign_path, 'w')
            flast.write(temp_id)
            flast.close()
        finally:
            id_tools.lock_alignment.release()

        return "alignment" + temp_id
