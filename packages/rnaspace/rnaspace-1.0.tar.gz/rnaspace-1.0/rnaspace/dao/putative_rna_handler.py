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


from data_handler import data_handler

class putative_rna_handler (data_handler):
    """ 
    Class putative_rna_handler: this data handler control all the data 
    dealing with a putative_rna
    """

    def __init__(self):
        data_handler.__init__(self)
    
    def get_putative_rna(self, user_id, rna_id, project_id):
        """
        Return(putative_rna)      the putative_rna defined by its id,
                                  None if no match

        user_id(type:string)      user id of the connected user
        rna_id(type:string)       the putative_rna id
        project_id(type:string)   project id the user is working on
        """
        raise NotImplementedError

    def get_putative_rnas(self, user_id, project_id = 0, run_id=None):
        """ 
        Return([putative_rna])    table of putative_rna for the 
                                  specified user and project 

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        run_id(type:string)       if specified return the run's putative_rnas,
                                  all of them are returned back otherwise
        """
        raise NotImplementedError

    def get_putative_rnas_by_runs(self, user_id, project_id):
        """ 
        Return([putative_rna])    table of putative_rna by run for the specified user
                                  and project

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        """
        raise NotImplementedError
    
    def delete_putative_rnas(self, user_id, project_id, rnas_id):
        """ 
        Delete a table of putative_rna specified by a user_id, 
        a project_id and their id.

        user_id(type:string)      user id of the connected user
        rnas_id(type:[string])    table of rna's id to delete
        project_id(type:string)   project id the user is working on
        """
        raise NotImplementedError    

    def delete_run(self, user_id, project_id, run_id):
        """ 
        Delete all information on run_id and putative_rnas linked
        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        run_id(type:[string])     the run_id
        """
        raise NotImplementedError  

    def update_putative_rna(self, user_id, project_id, rna_id, rna):
        """ 
        Update the whole rna specified by its id

        user_id(type:string)         user id of the connected user
        project_id(type:string)      project id the user is working on
        rna_id(type:string)          the rna id to update
        rna(type:core.putative_rna)  the rna with the value to update
        """
        raise NotImplementedError  

    def update_putative_rnas_family(self, user_id, project_id, rnas_id,
                                    new_family):
        """ 
        update the family of putative_rna specified by a user_id,
        a project_id and their id.

        user_id(type:string)      user id of the connected user
        rnas_id(type:[string])    table of rna's id to delete
        new_family(type:string)   the new family value
        project_id(type:string)   project id the user is working on
        """
        raise NotImplementedError  
    
    def add_putative_rnas(self, user_id, project_id, prnas):
        """ 
        Add a table of putative_rnas to the project
        
        user_id(type:string)       user id of the connected user
        project_id(type:string)    project id the user is working on
        prna(type:[putative_rna])  the putative rnas objects to add
        """
        raise NotImplementedError

    
