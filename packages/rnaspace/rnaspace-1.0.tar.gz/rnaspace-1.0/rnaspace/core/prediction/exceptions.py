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

class PredictorsConfError(Exception):
    """
    Exception raised when there is an error in the predictor 
    configuration files 

    Attributes:
      predictor -- predictor name
      section --  the name of the concerned section
      option -- the problematic option
    """

    def __init__(self, predictor, section, option=""):
        self.predictor = predictor
        self.section = section
        self.option = option

    def __str__(self):
        if self.option == "":
            return "\n\n section [" + self.section + "] does not exists in " +\
                self.predictor + " file !"

        return "\n\nFile:" + str(self.predictor) + "\n **section:[" +\
            str(self.section) + "]\n" + ' ****option "' + str(self.option) +\
            '" does not exists or contains error\n'


class PredictorsDirectoryError(Exception):
    """
    Exception raised when there is an error in the predictors 
    directory tree

    Attributes:
      dir --  the name of the concerned directory
      root -- root directory of predictors conf files
    """

    def __init__(self, dir, root):
        self.dir = dir
        self.root = root

    def __str__(self):
       return self.dir + " directory does not exist in " + self.root + " !"  
