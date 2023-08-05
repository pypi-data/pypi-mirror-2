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
import threading
try:
    import cPickle as pickle
except ImportError:
    import pickle

from putative_rna_handler import putative_rna_handler
from user_handler import user_handler

class dump_putative_rna_handler(putative_rna_handler):
    """
    Class dump_putative_rna_handler: this data handler control 
    all the data dealing with a putative_rna using serialize files
    """

    # lock objects to protect threads shared files 
    lock_dump = threading.Lock()

    def __init__(self):
        putative_rna_handler.__init__(self)
        self.user_handler = user_handler()


    def __delete_dump_file(self, user_id, rna, project_id):
        """ 
        Delete a putative_rna specified by a user_id, a project_id.

        user_id(type:string)         user id of the connected user
        rna(type:putative_rna)       the putative_rna object to delete
        project_id(type:string)      project id the user is working on
        """

        rnas_directory = self.config.get_putative_rna_directory(user_id,
                                                                project_id)
        temp = os.path.join(rnas_directory, rna.run)
        dump_file = os.path.join(temp, rna.sys_id + ".dump")
        size = os.path.getsize(dump_file)
        try:
            os.remove(dump_file)
            return size
        except OSError:
            pass


    def __update_dump_file(self, user_id, project_id, rna):
        """ 
        Update a putative_rna specified by a user_id, a project_id .

        user_id(type:string)         user id of the connected user
        rna(type:putative_rna)       the putative_rna object to delete
        project_id(type:string)      project id the user is working on
        """

        try:
            deleted_size = self.__delete_dump_file(user_id, rna, project_id)
            rnas_directory = self.config.get_putative_rna_directory(user_id,
                                                                    project_id)
            temp = os.path.join(rnas_directory, rna.run)
            dump_file = os.path.join(temp, rna.sys_id + ".dump")
            fdump = open(dump_file, "wb")
            pickle.dump(rna, fdump)
            fdump.close()
            added_size = os.path.getsize(dump_file)
            return added_size-deleted_size
        except:
            pass

    def __update_family_into_dump_file(self, user_id, rna, new_family,
                                       project_id):
        """ 
        user_id(type:string)         user id of the connected user
        rna(type:putative_rna)       the putative_rna object to delete
        new_family(type:string)      the new family value
        project_id(type:string)      project id the user is working on
        """

        rnas_directory = self.config.get_putative_rna_directory(user_id, 
                                                                project_id)
        temp = os.path.join(rnas_directory, rna.run)
        dump_file = os.path.join(temp, rna.sys_id + ".dump")
        old_size = os.path.getsize(dump_file)

        # read old rna
        fdump = open(dump_file, "rb")
        rna = pickle.load(fdump)
        fdump.close()

        # update family
        rna.family = new_family

        # write the new rna
        fdump = open(dump_file, "wb")
        pickle.dump(rna, fdump)
        fdump.close()
        new_size = os.path.getsize(dump_file)

        return new_size-old_size

    def get_putative_rna(self, user_id, rna_id, project_id):
        """
        Return(putative_rna)      the putative_rna defined by its id, 
                                  None if no match

        user_id(type:string)      user id of the connected user
        rna_id(type:string)       the putative_rna id
        project_id(type:string)   project id the user is working on
        """

        rna = None
        path = self.config.get_putative_rna_directory(user_id, project_id)
        if path != None:
            for runs in os.listdir(path):
                # if it's a run directory
                rpath = os.path.join(path, runs)
                if re.search("r.*", runs) or re.search("explore.*", runs): 
                    if os.path.isdir(rpath):
                        dump_file = os.path.join(rpath, rna_id + ".dump")
                        if os.path.isfile(dump_file):
                            fdump = open(dump_file, "rb")
                            rna = pickle.load(fdump)
                            fdump.close()
                            break
        return rna

    def get_putative_rna_directory(self, user_id, project_id):
        """
        Return(string)            return the putative rna directory
        
        user_id(string)           user id of the connected user
        project_id(string)        project id the user is working on
        """

        return self.config.get_putative_rna_directory(user_id, project_id)


    def get_putative_rnas(self, user_id, project_id, run_id = None):
        """ 
        Return([putative_rna])    table of putative_rna for the specified user
                                  and project

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        run_id(type:string)       if specified return the run's putative_rnas,
                                  all of them are returned back otherwise
        """

        putative_rnas = {}
        path = self.config.get_putative_rna_directory(user_id, project_id)
        if path != None:
            for run in os.listdir(path):
                # if it's a run directory
                if os.path.isdir(os.path.join(path, run)):
                    for dump in os.listdir(os.path.join(path, run)):            
                        dumppath = os.path.join(path, run)
                        dumppath = os.path.join(dumppath, dump)
                        if (re.search(".*.dump", dump) and 
                            os.path.isfile(dumppath)): 
                            fdump = open(dumppath, "rb")
                            rna = pickle.load(fdump)
                            fdump.close()                            
                            putative_rnas.setdefault(run, [])
                            putative_rnas[run].append(rna)

        prnas = []
        try:
            if run_id == None:
                for run in putative_rnas:
                    prnas.extend(putative_rnas[run])
            else:
                prnas.extend(putative_rnas[run_id])
        except:
            pass
        return prnas

    def get_putative_rnas_by_runs(self, user_id, project_id):
        """ 
        Return([putative_rna])    table of putative_rna by run for the specified user
                                  and project

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        """

        putative_rnas = {}
        path = self.config.get_putative_rna_directory(user_id, project_id)
        if path != None:
            for run in os.listdir(path):
                # if it's a run directory
                if os.path.isdir(os.path.join(path, run)):
                    for dump in os.listdir(os.path.join(path, run)):            
                        dumppath = os.path.join(path, run)
                        dumppath = os.path.join(dumppath, dump)
                        if(re.search(".*.dump", dump) and 
                           os.path.isfile(dumppath)): 
                            fdump = open(dumppath, "rb")
                            rna = pickle.load(fdump)
                            fdump.close()                            
                            putative_rnas.setdefault(run, [])
                            putative_rnas[run].append(rna)
        return putative_rnas

        
    def delete_putative_rnas(self, user_id, project_id, rnas_id):
        """ 
        Delete a table of putative_rna specified by a user_id, a project_id and
        their id. 

        user_id(type:string)         user id of the connected user
        rnas_id(type:[string])       table of rna's id to delete
        project_id(type:string)      project id the user is working on
        """

        putative_rnas = self.get_putative_rnas(user_id, project_id)
        size = 0
        for rna_id in rnas_id:
            for i in range(len(putative_rnas)):
                if putative_rnas[i].sys_id == rna_id:
                    # delete the file
                    size = size - self.__delete_dump_file(user_id,
                                                          putative_rnas[i],
                                                          project_id)

        self.user_handler.update_project_used_space(user_id, project_id, size)
    
    def delete_run(self, user_id, project_id, run_id):
        """ 
        Delete all information on run_id and putative_rnas linked
        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        run_id(type:[string])     the run_id
        """

        try:
            run_path = self.config.get_putative_rna_directory(user_id, project_id)
            run_path += "/" + run_id
            for files in os.listdir(run_path):
                path = run_path + "/" + files
                os.remove(path)
            os.removedirs(run_path)
        except:
            pass

    def update_putative_rna(self, user_id, project_id, rna_id, rna):
        """ 
        Update the whole rna specified by its id
        user_id(type:string)         user id of the connected user
        project_id(type:string)      project id the user is working on
        rna_id(type:string)          the rna id to update
        rna(type:core.putative_rna)  the rna with the value to update
        """

        size = self.__update_dump_file(user_id, project_id, rna)        
        self.user_handler.update_project_used_space(user_id, project_id, size)


    def update_putative_rnas_family(self, user_id, project_id, rnas_id, 
                                    new_family):
        """ 
        user_id(type:string)      user id of the connected user
        rnas_id(type:[string])    table of rna's id to delete
        new_family(type:string)   the new family value
        project_id(type:string)   project id the user is working on
        """

        putative_rnas = self.get_putative_rnas(user_id, project_id)
        size = 0
        for rna_id in rnas_id:
            for i in range(len(putative_rnas)):
                if putative_rnas[i].sys_id == rna_id:
                    size += self.__update_family_into_dump_file(user_id, 
                                                                putative_rnas[i],
                                                                new_family,
                                                                project_id)

        self.user_handler.update_project_used_space(user_id, project_id, size)

    def add_putative_rnas(self, user_id, project_id, prnas):
        """ 
        Add putative rnas to the project
        
        user_id(type:string)       user id of the connected user
        project_id(type:string)    project id the user is working on
        prna(type:[putative_rna])  the putative rna object to add
        """

        size = 0
        self.lock_dump.acquire()
        try:            
            p_rna_dir = self.config.get_putative_rna_directory(user_id, 
                                                               project_id)
            run_dir = os.path.join(p_rna_dir, prnas[0].run)
            if not os.path.isdir(run_dir):
                os.mkdir(run_dir)
            for prna in prnas:
                dump_file = os.path.join(run_dir, prna.sys_id + ".dump")
                fdump = open(dump_file, "wb")
                pickle.dump(prna, fdump)
                fdump.close()
                size = size + os.path.getsize(dump_file)

            self.user_handler.update_project_used_space(user_id, project_id,
                                                        size)
            self.lock_dump.release()            
        except:
            self.lock_dump.release()


    def get_putative_rna_path(self, user_id, project_id, run_id, p_rna_id):
        """
        Return(type:string)       path to the putative RNA dir

        user_id(type:string)      id of the connected user
        project_id(type:string)   id of the current project
        run_id(type: string)      id of the current run
        seq_id(type:string)       id of the sequence
        softname(type:string)     name of the predictor
        type(type:string)         predictor type
        """

        p_rna_dir = self.config.get_putative_rna_directory(user_id, project_id)
        path = os.path.join(p_rna_dir, run_id)
        path = os.path.join(path, p_rna_id + '.dump')
        return path
