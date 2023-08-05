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

class predictors_handler (data_handler):
    """
    Class predictors_handler: this data handler control all the data dealing
    with predictors log
    """

    def __init__(self):
        data_handler.__init__(self)

    def get_stdout_path(self, user_id, project_id, run_id, 
                        seq_id, softname, type):
        """
        Return(type:string)       the path of the stdout file

        user_id(type:string)      id of the connected user
        project_id(type:string)   id of the current project
        run_id(type: string)      id of the current run
        seq_id(type:string)       id of the sequence
        softname(type:string)     name of the predictor
        type(type:string)         predictor type
        """
        tmp_dir = self.config.get("storage", "tmp_dir")
        tmp_name = user_id + project_id + run_id + seq_id + softname +\
            type + ".stdout"
        return os.path.join(tmp_dir, tmp_name)
        
    def get_stderr_path(self, user_id, project_id, run_id, 
                        seq_id, softname, type):
        """
        Return(type:string)       the path of the stderr file

        user_id(type:string)      id of the connected user
        project_id(type:string)   id of the current project
        run_id(type: string)      id of the current run
        seq_id(type:string)       id of the sequence
        softname(type:string)     name of the predictor
        type(type:string)         predictor type
        """
        tmp_dir = self.config.get("storage", "tmp_dir")
        tmp_name = user_id + project_id + run_id + seq_id + softname +\
            type + ".stderr"
        return os.path.join(tmp_dir, tmp_name)



        
