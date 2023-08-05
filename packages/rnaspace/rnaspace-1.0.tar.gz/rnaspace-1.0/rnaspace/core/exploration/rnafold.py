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


import re
import subprocess
import tempfile
import logging

from rnaspace.core.secondary_structure import secondary_structure
from rnaspace.core.data_manager import data_manager
from rnaspace.core.email_sender import email_sender
from rnaspace.core.trace.event import error_event

class rnafold(object):
    """ Class rnafold: in charge to execute rnafold and parse its result file
    """
    
    def run(self, sequence, user_id, project_id):
        dm = data_manager()
        rnafold_exe = dm.get_rnafold_exe()
        tmp_file_name = tempfile.NamedTemporaryFile().name
        tmp_output_name = tempfile.NamedTemporaryFile().name
        tmp_file = open(tmp_file_name, 'a')
        tmp_file.write(sequence)
        tmp_file.close()
        rnafold_cmd = rnafold_exe + " <" + tmp_file_name + "> " + tmp_output_name

        retcode = subprocess.call(rnafold_cmd, shell=True)    
        if retcode == 0:             
            structure = self.__parse_rnafold_result(tmp_output_name)
        else:
            structure = ''
            message = "Problem running RNAfold: " + rnafold_cmd
            email_sender().send_admin_failed_email(user_id, project_id, \
                                                   "explore", "rnafold", rnafold_cmd) 
            mail = self.dm.get_user_email(user_id, project_id)
            ev = error_event(user_id, project_id, mail, 
                             message, self.data_m.get_project_size(user_id, project_id))
            logging.getLogger("rnaspace").error(ev.get_display())

        return structure
    
    def __parse_rnafold_result(self, tmp_output_name):
        f = open(tmp_output_name, 'r')
        for line in f.readlines():
            if re.search("[.()]", line):
                fields = line.rstrip().split()
                str = fields[0]
                str.replace("\n", "")
                free_energy = fields[1][1:len(fields[1])-1]
        structure = secondary_structure("brackets", str, "RNAfold", free_energy)
        return structure
