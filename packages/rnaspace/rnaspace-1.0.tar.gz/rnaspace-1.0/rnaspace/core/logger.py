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

import logging

from rnaspace.dao.storage_configuration_reader import storage_configuration_reader

def init():
    config = storage_configuration_reader()

    is_console_logging = config.get("logging", "log_into_console")
    log_file = config.get("logging", "rnaspace_log_file")
    log_file_handler = logging.FileHandler(log_file)
    log_file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(message)s")
    log_file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger("rnaspace")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_file_handler)
    if is_console_logging.lower() == "true":
        logger.addHandler(console_handler)
        


