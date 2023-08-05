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


class threads_manager:
    
    def __init__(self):
        self.threads = {}
        self.semaphores = {}

        
    def add_thread(self, user_id, project_id, run_id, t):
        """ 
        add thread in running threads dictionnary

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the id of the current run
        """
        self.threads.setdefault(user_id, {})
        self.threads[user_id].setdefault(project_id, {})
        self.threads[user_id][project_id].setdefault(run_id, [])
        self.threads[user_id][project_id][run_id].append(t)

    def run_threads_finished(self, user_id, project_id, run_id):
        """
        Return(type:boolean)   True if the execution of all selected
                               predictors has finished, False otherwise

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the id of the current run
        """
        try:
            for t in self.threads[user_id][project_id][run_id]:
                if t.isAlive():
                    return False
            self.remove_threads(user_id, project_id, run_id)
            return True
        except (KeyError, AttributeError):
            return True
        
    def get_threads(self, user_id, project_id, run_id):
        try:
            return self.threads[user_id][project_id][run_id]
        except (KeyError, AttributeError):
            return []

    def remove_threads(self, user_id, project_id, run_id):        
        run_threads = self.threads[user_id][project_id]        
        del run_threads[run_id]
