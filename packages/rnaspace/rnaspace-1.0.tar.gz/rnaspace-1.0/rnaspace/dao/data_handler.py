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
from storage_configuration_reader import storage_configuration_reader

class data_handler (object):
    """ 
    Class data_handler: this object is the base object of data access object
    """

    def __init__(self):
        """ 
        Build a data_handler object defined by    
        config(storage_configuration_reader)    the configuration file      
        """
        self.config = storage_configuration_reader()
        self.blocksize = int(self.config.get("storage", "blocksize"))

    def get_disk_size(self, path):
        """
        return the real disk size of a given file path
        """
        try:
            filesize = os.path.getsize(path)
            return self.get_disk_size_from_size(filesize)
        except:
            return None

    def get_disk_size_from_size(self, filesize):
        """
        return the real disk size of a given file size
        """
                
        try:
            size_on_disk = (filesize/self.blocksize)*self.blocksize
            if filesize % self.blocksize != 0:
                size_on_disk += self.blocksize
            return size_on_disk
        except:
            return None
