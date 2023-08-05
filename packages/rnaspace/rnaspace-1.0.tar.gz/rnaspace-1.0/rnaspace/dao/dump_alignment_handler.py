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
import tempfile
try:
    import cPickle as pickle
except ImportError:
    import pickle

from data_handler import data_handler
from user_handler import user_handler

class dump_alignment_handler(data_handler):
    """
    Class alignment_handler: this data handler control all the data dealing with
    an alignment
    """

    def __init__(self):
        data_handler.__init__(self)
        self.user_handler = user_handler()
        
    def get_alignment_path(self, user_id, project_id, align_id):
        """
        Return(type:string)       path to the alignment dir

        user_id(type:string)      id of the connected user
        project_id(type:string)   id of the current project
        align_id(type:string)     id of the sequence
        """
        align_dir = self.config.get_alignment_directory(user_id, project_id)
        path = os.path.join(align_dir, align_id + '.dump')

        return path

    def get_alignment_directory(self, user_id, project_id):
        """
        Return(type:string)       the path to the alignment directory
        
        user_id(type:string)      id of the connected user
        project_id(type:string)   id of the current project
        """
        return self.config.get_alignment_directory(user_id, project_id)


    def add_alignments(self, user_id, project_id, alignments):
        """ 
        Add an alignment to the project
        
        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        align(type:alignement)    the alignment object to add
        """
        size = 0
        align_dir = self.config.get_alignment_directory(user_id, project_id)
        for align in alignments:
            align_path = os.path.join(align_dir, align.id + '.dump')
            output = open(align_path, "wb")
            pickle.dump(align, output)
            output.close()
            size += os.path.getsize(align_path)

        self.user_handler.update_project_used_space(user_id, project_id, size)

    def save_alignment_as_temporary(self, user_id, project_id, alignment):
        """ 
        Save the alignment but don't add it to the project
        
        user_id(type:string)       user id of the connected user
        project_id(type:string)    project id the user is working on
        alignment(type:alignement) the alignment object to add
        """
        tmp_dir = tempfile.gettempdir()
        align_path = os.path.join(tmp_dir, alignment.id + '.dump')
        fdump = open(align_path, "wb")
        pickle.dump(alignment, fdump)
        fdump.close()

    def delete_alignment(self, user_id, project_id, align_id):
        """ 
        delete an alignment to the project
        
        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        align_id(type:alignement)  the alignment id to delete
        """
        try:
            path = self.get_alignment_path(user_id, project_id, align_id)
            size = os.path.getsize(path)
            os.remove(path)
            self.user_handler.update_project_used_space(user_id, project_id,
                                                        -size)
        except:
            pass

    def get_alignment(self, user_id, project_id, align_id):
        """
        Return(type:string)       the alignment
        user_id(string)           the id of the current user
        project_id(type:string)   project id the user is working on
        align_id(type:string)     the alignement id to return
        """

        path = self.get_alignment_path(user_id, project_id, align_id)
        if os.path.isfile(path):
            try:
                output = open(path, 'rb')
                align = pickle.load(output)
                output.close()
                return align
            except:
                return None

    def get_temporary_alignment(self, user_id, project_id, align_id):
        """
        Return(type:string)       the temporary alignment
        user_id(string)           the id of the current user
        project_id(type:string)   project id the user is working on
        align_id(type:string)     the alignement id to return
        """

        tmp_dir = tempfile.gettempdir()
        align_path = os.path.join(tmp_dir, align_id + '.dump')
        if os.path.isfile(align_path):
            try:
                output = open(align_path, 'rb')
                align = pickle.load(output)
                output.close()
                return align
            except:
                return None

        return None

    def get_alignments(self, user_id, project_id):
        """
        Return(type:string)       all project's alignments 
        user_id(string)           the id of the current user
        project_id(type:string)   project id the user is working on
        """

        aligns = []
        align_directory = self.get_alignment_directory(user_id, project_id)
        if align_directory != None:
            for align in os.listdir(align_directory):
                dumppath = os.path.join(align_directory, align)
                if(re.search(".*.dump", dumppath) and 
                   os.path.isfile(dumppath)):
                    output = open(dumppath, 'rb')
                    align = pickle.load(output)
                    output.close()
                    aligns.append(align)

        return aligns

    def get_nb_alignments(self, user_id, project_id):
        """
        Return(type:int)          the number of alignments in the current project
        user_id(string)           the id of the current user
        project_id(type:string)   project id the user is working on
        """
        nb_align = 0
        align_directory = self.get_alignment_directory(user_id, project_id)
        if align_directory != None:
            for align in os.listdir(align_directory):
                dumppath = os.path.join(align_directory, align)
                if(re.search(".*.dump", dumppath) and 
                   os.path.isfile(dumppath)):
                    nb_align += 1
        return nb_align

