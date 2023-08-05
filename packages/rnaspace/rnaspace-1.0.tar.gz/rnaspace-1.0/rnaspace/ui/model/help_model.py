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


from rnaspace.core.prediction.software_manager import software_manager
from rnaspace.core.data_manager import data_manager
import rnaspace.core.common as common

class help_model(object):
    
    HELP_CONTENT = None

    def __init__(self):
        self.sm = software_manager()
        self.data_m = data_manager()

    def get_sequence_size_limitation(self):
        nb_octets = self.data_m.get_sequence_size_limitation()
        size = common.get_octet_string_representation(nb_octets)
        return size

    def get_nb_sequence_limitation(self):
        return self.data_m.get_nb_sequences_limitation()

    def get_predictors_help(self):
        known_homology = self.sm.get_software_help("known_homology")
        known_rna_motif = self.sm.get_software_help("known_rna_motif")
        known_specialized = self.sm.get_software_help("known_specialized")
        comparative = self.sm.get_software_help("inference")
        abinitio = self.sm.get_software_help("abinitio")

        return (known_homology, known_rna_motif, known_specialized,
                comparative, abinitio)

    def get_predictors_description(self):
        d_known = self.sm.get_software_desc("known")
        d_comparative = self.sm.get_software_desc("inference")
        d_abinitio = self.sm.get_software_desc("abinitio")

        return (d_known, d_known, d_known, d_comparative, d_abinitio)

    def get_mount_point(self):
        return self.data_m.get_mount_point()
