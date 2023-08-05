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

from data_handler import data_handler

class database_handler(data_handler):
    """
    This class gathers all information about databases.
    """
    
    # dictionary containing db names and paths
    databases_names = {}

    def __init__(self):
        data_handler.__init__(self)
        self.databases_directory = self.config.get_databases_directory()
        if database_handler.databases_names == {}:
            self.load_db()

    def load_db(self):
        """
        Load availabe databases and put their {name:path} in 
        databases_names dictionary
        """
        if self.databases_directory is None:
            return        
        # for all files in the databases directory 
        for entry in os.listdir(self.databases_directory):
            # if it is not a directory
            if os.path.isfile(os.path.join(self.databases_directory, entry)):
                # get the file name (relative path)
                (filepath, filename) = os.path.split(entry)
                # get the name without extension
                (shortname, ext) = os.path.splitext(filename)
                # if the file is a multifasta file
                if ext == '.nin':
                    # then we add the database to the dictionary
                    db_path = os.path.join(self.databases_directory, shortname)
                    database_handler.databases_names[shortname] = db_path
 
    def get_db_path(self, dbase):
        """
        Return(string)    the path of the database named db, None if
                          if doesn't exist
        
        db(string)        the name of the db
        """
        if database_handler.databases_names.has_key(dbase):
            return database_handler.databases_names[dbase]
        else:
            return None
    
    def get_db_names(self):
        """
        Return([string])    the list of available databases 
        """
        if database_handler.databases_names == {}:
            self.load_db()
        if database_handler.databases_names == {}:
            return None
        return database_handler.databases_names.keys()

    def get_system_db_name(self, path):
        """
        Return(string)    the database system name for the specified path

        path(string)      the path of the databases
        """
        try:
            # we just take the name of the file and return it with a "%" prefix
            (filepath, filename) = os.path.split(path)
            (shortname, ext) = os.path.splitext(filename)
            return "%" + shortname
        except:
            return "unknown"

    def get_system_db_sequence_name(self, seq_name):
        """
        Return(string)    the sequence system name

        seq_name(string)  the sequence name
        """
        return "%" + seq_name

    def get_cluster_file(self, dbname):
        return dbname + "_cluster.txt"
