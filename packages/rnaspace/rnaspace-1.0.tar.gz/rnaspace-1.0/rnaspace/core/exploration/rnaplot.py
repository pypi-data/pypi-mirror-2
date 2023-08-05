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
import subprocess
import tempfile
import logging

from rnaspace.core.data_manager import data_manager
from rnaspace.core.email_sender import email_sender
from rnaspace.core.trace.event import error_event

class rnaplot(object):
    """ Class rnaplot: in charge to execute rnaplot and parse its result file
    """

    def run(self, user_id, project_id, sequence, structure, output, format = "png"):
        returned_file = None
        logger = logging.getLogger("rnaspace")
        dm = data_manager()
        rnaplot_exe = dm.get_rnaplot_exe()
        tmp_dir = dm.config.get("storage","tmp_dir")
        tmp_file_name = tempfile.NamedTemporaryFile(dir=tmp_dir).name
        tmp_output_name = tempfile.NamedTemporaryFile(dir=tmp_dir).name
        tmp_output_file = os.path.dirname(tmp_output_name)
        # only the first 6 characters are considered by RNAplot for output name
        tmp_output_name = os.path.basename(tmp_output_name)[0:6] 
        tmp_output_name = tmp_output_file + "/" + tmp_output_name
        tmp_file = open(tmp_file_name, 'a')
        tmp_file.write(">" + os.path.basename(tmp_output_name) +  "\n")        
        tmp_file.write(sequence)
        tmp_file.write("\n")
        tmp_file.write(structure.structure)
        tmp_file.close()
        tmp_tmp = tempfile.NamedTemporaryFile(dir=tmp_dir).name
        rnaplot_cmd = rnaplot_exe + " <" + tmp_file_name + " 1>" + tmp_tmp + " 2>" + tmp_tmp
        retcode = subprocess.call(rnaplot_cmd, shell=True, cwd=tmp_dir)
        if retcode != 0:
            message = "Problem running RNAplot: " + rnaplot_cmd
            email_sender().send_admin_failed_email(user_id, project_id, \
                                                   "explore", "rnaplot", rnaplot_cmd) 
            mail = dm.get_user_email(user_id, project_id)
            ev = error_event(user_id, project_id, mail, 
                             message, dm.get_project_size(user_id, project_id))
            logger.error(ev.get_display())
        else:
            convert_cmd = "convert " + tmp_output_name + "_ss.ps " + os.path.join(output, os.path.basename(tmp_output_name) + "." + format)
            retcode = subprocess.call(convert_cmd, shell=True)
            if retcode != 0:
                message = "Problem running convert: " + convert_cmd
                email_sender().send_admin_failed_email(user_id, project_id, \
                                                       "explore", "rnaplot", convert_cmd)
                mail = dm.get_user_email(user_id, project_id)
                ev = error_event(user_id, project_id, mail, 
                             message, dm.get_project_size(user_id, project_id))
                logger.error(ev.get_display())
            else:
                returned_file = os.path.basename(tmp_output_name) + "." + format
        return returned_file
