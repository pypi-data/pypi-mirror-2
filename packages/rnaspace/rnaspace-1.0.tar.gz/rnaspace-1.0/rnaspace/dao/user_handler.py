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

from data_handler import data_handler
from rnaspace.core.id_tools import id_tools

class user_handler (data_handler):
    """
    Class user_handler: this data handler control all the data dealing with
    the user
    """
    # lock objects to protect threads shared files 
    lock_dump = threading.Lock()
    
    def __init__(self):
        data_handler.__init__(self)

    def has_data(self, user_id):
        """ 
        Return(type:boolean)      True if the user has data on disk, else False

        user_id(type:string)      user id of the connected user
        """

        return self.config.get_user_directory(user_id) != None

    def has_project(self, user_id, project_id):
        """ 
        Return(type:boolean)      True if the user has the specified project, False otherwise
        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        """
        return self.config.get_project_directory(user_id, project_id) != None

    def user_has_done_a_run(self, user_id, project_id):
        """ 
        Return(type:boolean)      True if the user has done a run on the specified project, False otherwise
        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        """
        putative_dir = self.config.get_putative_rna_directory(user_id, project_id)
        return len(os.listdir(putative_dir)) != 0

    def new_project(self, user_id):
        """
        Create necessary directories for a new project

        Return(type:string)      the id of the new project

        user_id(type:string)     id of the connected user
        """
        id_t = id_tools()
        user_dir = self.config.get_user_directory(user_id)
        if user_dir is None:
            stock = self.config.get_storage_directory()
            user_dir = os.path.join(stock, user_id)
            os.mkdir(user_dir)
        project_id = id_t.get_new_project_id(user_id)
        project_path = os.path.join(user_dir, project_id)
        os.mkdir(project_path)
        os.mkdir(os.path.join(project_path, 'sequence'))
        os.mkdir(os.path.join(project_path, 'putative_rna'))
        os.mkdir(os.path.join(project_path, 'alignment'))

        return project_id

    def new_run(self, user_id, project_id):
        """
        Create necessary directory for a new run

        Return(type:string)     the id of the new run
        
        user_id(type:string)    id of the connected user
        project_id(type:string) id of the current project
        """
        id_t = id_tools()
        run_id = id_t.get_new_run_id(user_id, project_id)
        putative_dir = self.config.get_putative_rna_directory(user_id, 
                                                              project_id)
        os.mkdir(os.path.join(putative_dir, run_id))

        return run_id

    def get_user_directory(self, user_id):
        """
        Return(string)           the path to the user directory

        user_id(string)          id of the connected user
        """
        return self.config.get_user_directory(user_id)

    def get_project_directory(self, user_id, project_id):
        """
        Return(string)           the path to the project directory

        user_id(string)          id of the connected user
        project_id(string)       id of the project the user is working on
        """
        return self.config.get_project_directory(user_id, project_id)

    def get_ids_from_authkey(self, id):
        """
        id(sting)      the id containing the user_id and the project_id
        return [user_id, project_id]
        """
        infos = id.split("-")
        
        if len(infos) != 2:
            return (None, None)        
        user_dir = self.get_user_directory(infos[0])
        if user_dir is None:
            return (None, None)        
        project_dir = self.get_project_directory(infos[0], infos[1])
        if project_dir is None or len(infos[1]) == 0:
            return (None, None)        
        return infos
        
    def get_authkey(self, user_id, project_id):
        """
        user_id(sting)      the user_id
        project_id(string)  the project_id
        return the id
        """
        return user_id + "-" + project_id


    def get_user_informations_file(self, user_id):
        """
        Return(type:string)     the path to the user used space file 

        user_id(type:string)    the user id
        """
        user_dir = self.get_user_directory(user_id)
        if user_dir is not None:
            user_info = os.path.join(user_dir, user_id + ".txt")
            return user_info
        else:
            return None

    def __get_user_information(self, user_id, info):
        """
        Read the user informations file and look for the value of 'info'
        
        Return(string)       the value of the opt 'info', None if 'info' not in
                             the file

        user_id(string)      the user id
        info(string)         the information we want
        """
        self.lock_dump.acquire()
        try:
            user_info_file = self.get_user_informations_file(user_id)
            information = None
            if os.path.isfile(user_info_file):
                fuif = open(user_info_file, "r")
                content = fuif.read()
                fuif.close()
                content = content.splitlines()
                for line in content:
                    opt = line.split("=")[0]
                    val = line.split("=")[1].replace("\n", "")
                    if opt == info:
                        information = val
                self.lock_dump.release()
                return information
            else:
                self.lock_dump.release()
                return None
        except:
            self.lock_dump.release()
            return None

    def __update_information(self, user_id, info, info_val):
        """
        Update the 'info' entry with 'info_val' value in the user informations
        file
        
        user_id(string)      the user id
        info(string)         the information we want to update
        info_val(string)     the value of the info
        """
        
        self.lock_dump.acquire()
        try:
            user_info_file = self.get_user_informations_file(user_id)
            informations = {}
            # read the file if it exists
            if os.path.isfile(user_info_file):
                fuif = open(user_info_file, "r")
                content = fuif.read()
                fuif.close()
                content = content.splitlines()
                for line in content:
                    opt = line.split("=")[0]
                    val = line.split("=")[1].replace("\n", "")
                    informations[opt] = val
                
            # update the value
            informations[info] = info_val

            informations_keys = informations.keys()
            informations_keys.sort()
            # and write the updated file
            fuif = open(user_info_file, "w")
            for opt in informations_keys:
                fuif.write(str(opt) + "=" + str(informations[opt]) + "\n")
            fuif.close()
            self.lock_dump.release()
        except:
            self.lock_dump.release()
        

    def get_user_used_space(self, user_id):
        """
        Return(long)     the number of bytes that the user used

        user_id(string)  the user id
        """
        user_dir = self.get_user_directory(user_id)
        size = 0
        for f in os.listdir(user_dir):
            if os.path.isdir(os.path.join(user_dir, f)):
                project_id = f
                size += self.get_project_used_space(user_id, project_id)
        return size

    def get_user_last_project_id(self, user_id):
        """
        Return(long)         the last project id

        user_id(string)      the user id
        """

        last_id = self.__get_user_information(user_id, "last_project_id")
        if last_id is None:
            last_id = long(0)
        else:
            last_id = long(last_id)
        return last_id

    def update_user_last_project_id(self, user_id, project_id):
        """
        Update the last_project_id with the new one
        
        user_id(string)       the user id
        project_id(long)      the new project_id
        """
        self.__update_information(user_id, "last_project_id", project_id)
    




    def __get_project_information(self, user_id, project_id, info):
        """
        Read the user informations file and look for the value of 'info'
        
        Return(string)       the value of the opt 'info', None if 'info' not in
                             the file

        user_id(string)      the user id
        info(string)         the information we want
        """
        self.lock_dump.acquire()
        try:
            project_info_file = self.get_project_informations_file(user_id,
                                                                   project_id)
            information = None
            if os.path.isfile(project_info_file):
                fuif = open(project_info_file, "r")
                content = fuif.read()
                fuif.close()
                content = content.splitlines()
                for line in content:
                    opt = line.split("=")[0]
                    val = line.split("=")[1].replace("\n", "")
                    if opt == info:
                        information = val
                self.lock_dump.release()
                return information
            else:
                self.lock_dump.release()
                return None
        except:
            self.lock_dump.release()
            return None

    def __update_project_information(self, user_id, project_id, info, info_val):
        """
        Update the 'info' entry with 'info_val' value in the user informations
        file
        
        user_id(string)      the user id
        info(string)         the information we want to update
        info_val(string)     the value of the info
        """
        
        self.lock_dump.acquire()
        try:
            project_info_file = self.get_project_informations_file(user_id,
                                                                   project_id)
            informations = {}
            # read the file if it exists
            if os.path.isfile(project_info_file):
                fuif = open(project_info_file, "r")
                content = fuif.read()
                fuif.close()
                content = content.splitlines()
                for line in content:
                    opt = line.split("=")[0]
                    val = line.split("=")[1].replace("\n", "")
                    informations[opt] = val
                
            # update the value
            informations[info] = info_val

            informations_keys = informations.keys()
            informations_keys.sort()
            # and write the updated file
            fuif = open(project_info_file, "w")
            for opt in informations_keys:
                fuif.write(str(opt) + "=" + str(informations[opt]) + "\n")
            fuif.close()
            self.lock_dump.release()
        except:
            self.lock_dump.release()

    def get_project_informations_file(self, user_id, project_id):
        """
        Return(type:string)     the path to the project informations file 

        user_id(type:string)    the user id
        """
        project_dir = self.get_project_directory(user_id, project_id)
        if project_dir is not None:
            project_info = os.path.join(project_dir, project_id + ".txt")
            return project_info
        else:
            return None

    def get_project_used_space(self, user_id, project_id):
        """
        Return(long)         the number of bytes that is used for the project

        user_id(string)      the user id
        project_id(string)   the project id
        """

        size = self.__get_project_information(user_id, project_id, "used_space")
        if size is None:
            size = long(0)
        else:
            size = long(size)
        return size

    def get_project_sequences_used_space(self, user_id, project_id):
        """
        Return(long)         the number of bytes that is used for the sequences

        user_id(string)      the user id
        project_id(string)   the project id
        """
        size = self.__get_project_information(user_id, project_id,
                                              "sequences_used_space")
        if size is None:
            size = long(0)
        else:
            size = long(size)
        return size

    def update_project_used_space(self, user_id, project_id, size):
        """
        Update the project used space by adding size to the current size used

        user_id(string)       the user id
        project_id(string)    the project id
        size(long)            the number of bytes to add
        """

        current_size = self.get_project_used_space(user_id, project_id)
        new_size = current_size + size
        self.__update_project_information(user_id, project_id,
                                          "used_space", new_size)

    def update_project_sequences_used_space(self, user_id, project_id, size):
        """
        Update the user sequences used space by adding
        size to the current size used

        user_id(string)       the user id
        project_id(string)    the project id
        size(long)            the number of bytes to add
        """

        current_size = self.get_project_sequences_used_space(user_id,
                                                             project_id)
        new_size = current_size + size
        self.__update_project_information(user_id, project_id,
                                          "sequences_used_space", new_size)

    def get_user_email(self, user_id, project_id):
        """
        Return(string)           the email address

        user_id(string)          the id of the connected user
        """
        mail = self.__get_project_information(user_id, project_id, "email")
        return mail.split(',')
        
    def save_user_email(self, user_id, project_id, email):
        """
        Save the user email

        user_id(string)          the id of the connected user
        email(string)            the email address
        """
        self.__update_project_information(user_id, project_id, "email", email)

    def get_last_run_id(self, user_id, project_id):
        run_id = self.__get_project_information(user_id, project_id,
                                                "last_run_id")
        if run_id is None:
            return 0
        return int(run_id)

    def update_last_run_id(self, user_id, project_id, run_id):
        self.__update_project_information(user_id, project_id,  "last_run_id", run_id)
