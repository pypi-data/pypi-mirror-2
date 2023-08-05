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

from xml.dom.minidom import parse

import rnaspace.core.common as common
from rnaspace.core.conversion.rnaml import rnaml    
from putative_rna_handler import putative_rna_handler
from user_handler import user_handler
from rnaspace.core.exceptions import disk_error, project_space_error, user_space_error

class rnaml_putative_rna_handler (putative_rna_handler):
    """
    Class rnaml_putative_rna_handler: this data handler control 
    all the data dealing with a putative_rna using rnaml files
    """

    # lock objects to protect threads shared files 
    lock_dump = threading.Lock()

    def __init__(self):
        putative_rna_handler.__init__(self)
        self.user_handler = user_handler()

    def __serialize_putative_rnas(self, user_id, rnas, project_id, run_id):
        """ 
        Serialize the rnas table into the serialisation file linked to 
        the specified project and user

        user_id(type:string)      user id of the connected user
        rnas(type:[putative_rna]) putative_rnas to serialize
        project_id(type:string)   project id the user is working on
        """
        dump = self.config.get_putative_rna_serialization_file(user_id,
                                                               project_id,
                                                               run_id)
        f = open(dump, "wb")
        pickle.dump(rnas, f)
        f.close()        

    def __delete_rnaml_file(self, user_id, rna, project_id):
        """ 
        Delete a putative_rna specified by a user_id, a project_id.
        The rna will be deleted from the rnaml directory and 
        the serialization file.

        user_id(type:string)         user id of the connected user
        rna(type:putative_rna)       the putative_rna object to delete
        project_id(type:string)      project id the user is working on
        """
        rnas_directory = self.config.get_putative_rna_directory(user_id,
                                                                project_id)
        temp = os.path.join(rnas_directory, rna.run)
        rnaml_file = os.path.join(temp, rna.sys_id + ".xml")
        size = self.get_disk_size(rnaml_file)
        try:
            os.remove(rnaml_file)
            return size
        except OSError:
            pass


    def __update_rnaml_file(self, user_id, project_id, rna):
        """ 
        Update a putative_rna specified by a user_id, a project_id .

        user_id(type:string)         user id of the connected user
        rna(type:putative_rna)       the putative_rna object to delete
        project_id(type:string)      project id the user is working on
        """
        try:
            # First delete the old rnaml file
            deleted_size = self.__delete_rnaml_file(user_id, rna, project_id)
            # Then create a brand new one
            rnas_directory = self.config.get_putative_rna_directory(user_id,
                                                                    project_id)
            temp = os.path.join(rnas_directory, rna.run)
            rnaml_file = os.path.join(temp, rna.sys_id + ".xml")
            writer = rnaml()
            rnas = []
            rnas.append(rna)
            writer.write(rnas, rnaml_file)
            added_size = self.get_disk_size(rnaml_file)
            return added_size-deleted_size
        except:
            pass

    def __update_family_into_rnaml_file(self, user_id, rna, new_family,
                                        project_id):
        """ 
        Delete a putative_rna specified by a user_id, a project_id.
        The rna will be deleted from the rnaml directory and 
        the serialization file.

        user_id(type:string)         user id of the connected user
        rna(type:putative_rna)       the putative_rna object to delete
        new_family(type:string)      the new family value
        project_id(type:string)      project id the user is working on
        """
        rnas_directory = self.config.get_putative_rna_directory(user_id, 
                                                                project_id)
        temp = os.path.join(rnas_directory, rna.run)
        rnaml_file = os.path.join(temp, rna.sys_id + ".xml")
        old_size = self.get_disk_size(rnaml_file)
        xmldoc = parse (rnaml_file)
        # Seeking for the node to modify
        current_node = xmldoc.documentElement
        for attr in current_node.getElementsByTagName("molecule-class"):
            if attr.nodeType == attr.ELEMENT_NODE:
                try:                    
                    attr.getElementsByTagName("name")[0].childNodes[0].nodeValue = new_family
                except:
                    pass
        frnaml = open(rnaml_file, "w")
        frnaml.write(xmldoc.toxml())
        frnaml.close()
        new_size = self.get_disk_size(rnaml_file)
        return new_size-old_size

    def get_putative_rna(self, user_id, rna_id, project_id):
        """
        Return(putative_rna)      the putative_rna defined by its id, 
                                  None if no match

        user_id(type:string)      user id of the connected user
        rna_id(type:string)       the putative_rna id
        project_id(type:string)   project id the user is working on
        """
        reader = rnaml()
        rna = None
        path = self.config.get_putative_rna_directory(user_id, project_id)
        if path != None:
            for runs in os.listdir(path):
                # if it's a run directory
                rpath = os.path.join(path, runs)
                if re.search("r.*", runs) or re.search("explore.*", runs): 
                    if os.path.isdir(rpath):
                        rnaml_file = os.path.join(rpath, rna_id + ".xml")
                        if os.path.isfile(rnaml_file):
                            reader.read(rnaml_file)
                            rna = reader.get_putative_rna()
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
        reader = rnaml()
        path = self.config.get_putative_rna_directory(user_id, project_id)
        if path != None:
            for runs in os.listdir(path):
                # if it's a run directory
                if os.path.isdir(os.path.join(path, runs)):
                    dump = self.config.get_putative_rna_serialization_file(user_id, project_id, str(runs))
                    if not os.path.isfile(dump):
                        for xmls in os.listdir(os.path.join(path, runs)):
                            # if it's an xml file
                            xmlpath = os.path.join(path, runs)
                            xmlpath = os.path.join(xmlpath, xmls)
                            if (re.search(".*.xml", xmls) and 
                                os.path.isfile(xmlpath)): 
                                reader.read(xmlpath)
                                putative_rnas.setdefault(runs, [])
                                putative_rnas[runs].append(reader.get_putative_rna())

                        # serialize the result
                        if runs in putative_rnas:
                            fdump = open(dump, "wb")                        
                            pickle.dump(putative_rnas[runs], fdump)
                            fdump.close()
                    else: # The serialization has already been done
                        putative_rnas.setdefault(runs, [])
                        fdump = open(dump, "rb")
                        putative_rnas[runs].extend(pickle.load(fdump))
                        fdump.close()

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
        reader = rnaml()
        path = self.config.get_putative_rna_directory(user_id, project_id)
        if path != None:
            for runs in os.listdir(path):
                # if it's a run directory
                if re.search("run.*", runs) or re.search("explore.*", runs):                
                    if os.path.isdir(os.path.join(path, runs)):
                        dump = self.config.get_putative_rna_serialization_file(user_id, project_id, str(runs))
                        if not os.path.isfile(dump):
                            for xmls in os.listdir(os.path.join(path, runs)):
                                # if it's an xml file
                                xmlpath = os.path.join(path, runs)
                                xmlpath = os.path.join(xmlpath, xmls)
                                if (re.search(".*.xml", xmls) and 
                                    os.path.isfile(xmlpath)): 
                                    reader.read(xmlpath)
                                    putative_rnas.setdefault(runs, [])
                                    putative_rnas[runs].append(reader.get_putative_rna())
    
                            # serialize the result
                            if runs in putative_rnas:
                                fdump = open(dump, "wb")                        
                                pickle.dump(putative_rnas[runs], fdump)
                                fdump.close()
                        else: # The serialization has already been done
                            putative_rnas.setdefault(runs, [])
                            fdump = open(dump, "rb")
                            putative_rnas[runs].extend(pickle.load(fdump))
                            fdump.close()
        return putative_rnas
        
    def delete_putative_rnas(self, user_id, project_id, rnas_id):
        """ 
        Delete a table of putative_rna specified by a user_id, a project_id and
        their id. The rna will be deleted from the rnaml directory and the 
        serialization file.

        user_id(type:string)         user id of the connected user
        rnas_id(type:[string])       table of rna's id to delete
        project_id(type:string)      project id the user is working on
        """
        putative_rnas = self.get_putative_rnas(user_id, project_id)
        size = 0
        for rna_id in rnas_id:
            for i in range(len(putative_rnas)):
                if putative_rnas[i].sys_id == rna_id:
                    # Delete the rnaml file
                    size = size - self.__delete_rnaml_file(user_id,
                                                           putative_rnas[i],
                                                           project_id)
                    # Delete from the table
                    putative_rnas_current_run = \
                        self.get_putative_rnas(user_id, project_id, 
                                               putative_rnas[i].run)

                    for j in range(len(putative_rnas_current_run)):
                        if putative_rnas_current_run[j].sys_id == rna_id:
                            run = putative_rnas_current_run[j].run
                            del putative_rnas_current_run[j]
                            # Save the modification into the serialization file
                            self.__serialize_putative_rnas(user_id, 
                                                           putative_rnas_current_run, 
                                                           project_id, run)
                            break

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
        Raise disk_error if no more space available
        
        Update the whole rna specified by its id
        user_id(type:string)         user id of the connected user
        project_id(type:string)      project id the user is working on
        rna_id(type:string)          the rna id to update
        rna(type:rnaspace.core.putative_rna)  the rna with the value to update
        """

        max_user_size = common.get_nb_octet(self.config.get("storage", "user_size_limitation"))
        max_project_size = common.get_nb_octet(self.config.get("storage", "project_size_limitation"))
        user_space = self.user_handler.get_user_used_space(user_id)
        project_space = self.user_handler.get_project_used_space(user_id,
                                                                 project_id)
        if user_space > max_user_size:
            raise user_space_error(user_id, project_id, disk_error.prna_message)

        if project_space > max_project_size:
            raise project_space_error(user_id, project_id,
                                      disk_error.prna_message)

        
        putative_rnas = self.get_putative_rnas(user_id, project_id, rna.run)
        for i in range(len(putative_rnas)):
            if putative_rnas[i].sys_id == rna_id:
                del putative_rnas[i]
                putative_rnas.append(rna)
                break
        # Save the modification into the serialization file
        self.__serialize_putative_rnas(user_id, putative_rnas, project_id, 
                                       rna.run)
        # Save the modification into the rnaml file
        size = self.__update_rnaml_file(user_id, project_id, rna)
        
        self.user_handler.update_project_used_space(user_id, project_id, size)


    def update_putative_rnas_family(self, user_id, project_id, rnas_id, 
                                    new_family):
        """
        Raise disk_error if no more space available
        
        Delete a table of putative_rna specified by a user_id, a project_id 
        and their id.

        user_id(type:string)      user id of the connected user
        rnas_id(type:[string])    table of rna's id to delete
        new_family(type:string)   the new family value
        project_id(type:string)   project id the user is working on
        """

        max_user_size = common.get_nb_octet(self.config.get("storage", "user_size_limitation"))
        max_project_size = common.get_nb_octet(self.config.get("storage", "project_size_limitation"))
        user_space = self.user_handler.get_user_used_space(user_id)
        project_space = self.user_handler.get_project_used_space(user_id,
                                                                 project_id)

        if user_space > max_user_size:
            raise user_space_error(user_id, project_id, disk_error.prna_message)

        if project_space > max_project_size:
            raise project_space_error(user_id, project_id,
                                      disk_error.prna_message)
        
        putative_rnas = self.get_putative_rnas(user_id, project_id)
        size = 0
        for rna_id in rnas_id:
            for i in range(len(putative_rnas)):
                if putative_rnas[i].sys_id == rna_id:
                    # Update the rnaml file
                    size += self.__update_family_into_rnaml_file(user_id, 
                                                                 putative_rnas[i],
                                                                 new_family, project_id)
                    # Update the table
                    putative_rnas_current_run = \
                        self.get_putative_rnas(user_id, project_id, 
                                               putative_rnas[i].run)

                    for j in range(len(putative_rnas_current_run)):
                        if putative_rnas_current_run[j].sys_id == rna_id:
                            putative_rnas_current_run[j].family = new_family
                            # Save the modification into the serialization file
                            self.__serialize_putative_rnas(user_id, putative_rnas_current_run, project_id, putative_rnas_current_run[j].run)
                            break
        self.user_handler.update_project_used_space(user_id, project_id, size)

    def add_putative_rnas(self, user_id, project_id, prnas):
        """
        Raise disk_error if no more space available
        
        Add a putative_rnas to the project
        
        user_id(type:string)       user id of the connected user
        project_id(type:string)    project id the user is working on
        prna(type:[putative_rna])  the putative rna object to add
        """
        size = 0
        max_user_size = common.get_nb_octet(self.config.get("storage", "user_size_limitation"))
        max_project_size = common.get_nb_octet(self.config.get("storage", "project_size_limitation"))
        user_space = self.user_handler.get_user_used_space(user_id)
        project_space = self.user_handler.get_project_used_space(user_id,
                                                                 project_id)
        
        self.lock_dump.acquire()
        try:
            rnas_serial = []
            rnas_serial = self.get_putative_rnas(user_id, project_id,
                                                 prnas[0].run)
            
            p_rna_dir = self.config.get_putative_rna_directory(user_id,
                                                               project_id)
            run_dir = os.path.join(p_rna_dir, prnas[0].run)
            if not os.path.isdir(run_dir):
                os.mkdir(run_dir)
            for prna in prnas:
                if size + user_space > max_user_size:
                    self.__serialize_putative_rnas(user_id, rnas_serial,
                                                   project_id, prnas[0].run)
                    self.user_handler.update_project_used_space(user_id,
                                                                project_id,
                                                                size)           
                    raise user_space_error(user_id, project_id,
                                           disk_error.prna_message)

                if size + project_space > max_project_size:
                    self.__serialize_putative_rnas(user_id, rnas_serial,
                                                   project_id, prnas[0].run)
                    self.user_handler.update_project_used_space(user_id,
                                                                project_id,
                                                                size)       
                    raise project_space_error(user_id, project_id,
                                              disk_error.prna_message)

                rnaml_file = os.path.join(run_dir, prna.sys_id + ".xml")
                writer = rnaml()
                writer.write([prna], rnaml_file)
                size = size + self.get_disk_size(rnaml_file)
                rnas_serial.append(prna)
                



            self.__serialize_putative_rnas(user_id, rnas_serial, project_id,
                                           prnas[0].run)

            self.user_handler.update_project_used_space(user_id, project_id,
                                                        size)            
            self.lock_dump.release()
        except disk_error, e:
            self.lock_dump.release()
            raise e
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
        path = os.path.join(path, p_rna_id + '.xml')
        return path

#     def get_gff3_path(self, user_id, project_id, run_id, seq_id,
#                       alignsoft_name, program_name):
#         """
#         Return(type:string)             path to the gff3 dir

#         user_id(type:string)            id of the connected user
#         project_id(type:string)         id of the current project
#         run_id(type: string)            id of the current run
#         seq_id(type:string)             id of the sequence
#         alignsoft_name(type:string)     name of the alignment software used to
#                                         produce blast files
#         program_name(type:string)       name of the aggregation softwre used to
#                                         produce gff3 files
#         """

#         p_rna_dir = self.config.get_putative_rna_directory(user_id, project_id)
#         path = os.path.join(p_rna_dir, run_id)
#         if not os.path.isdir(path):
#             os.mkdir(path)
#         path = os.path.join(path, seq_id)
#         if not os.path.isdir(path):
#             os.mkdir(path)
#         path = os.path.join(path, alignsoft_name)
#         if not os.path.isdir(path):
#             os.mkdir(path)
#         path = os.path.join(path, program_name)
#         if not os.path.isdir(path):
#             os.mkdir(path)
#         return path

#     def get_gff3_parent_path(self, user_id, project_id, run_id, seq_id,
#                              alignsoft_name):
#         """
#         Return(string)                  the path to the gff3 parent directory

#         user_id(type:string)            id of the connected user
#         project_id(type:string)         id of the current project
#         run_id(type: string)            id of the current run
#         seq_id(type:string)             id of the sequence
#         alignsoft_name(type:string)     name of the alignment software used to
#                                         produce blast files
#         """
#         p_rna_dir = self.config.get_putative_rna_directory(user_id, project_id)
#         path = os.path.join(p_rna_dir, run_id)
#         path = os.path.join(path, seq_id)
#         path = os.path.join(path, alignsoft_name)
#         return path
