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

import cherrypy

from rnaspace.ui.utils.common import common
from rnaspace.ui.model.help_model import help_model

class help_controller(object):

    def __init__(self):
        self.model = help_model()
        self.view = common.get_template('help_view.tmpl')
        self.content = common.get_template('help.tmpl')
        self.toc = common.get_template('help_toc_view.tmpl')

    def alphabetical_sort(self, softs):
        temp_softs = [ (soft.lower(), i, soft) for i, soft in enumerate(softs)]
        temp_softs.sort()
        return temp_softs

    @cherrypy.expose
    def index(self):
        predictor = common.get_template('help_predictors_detailed_view.tmpl')
        #content = Template(self.model.get_help_content())
        (known_homology, known_rna_motif, known_specialized, comparative,
         abinitio) = self.model.get_predictors_help()

        (d_known_homology, d_known_rna_motif, d_known_specialized, d_comparative,
         d_abinitio) = self.model.get_predictors_description()

        # sort by alphabetical order        
        sorted_known_homology = self.alphabetical_sort(known_homology)
        sorted_known_rna_motif = self.alphabetical_sort(known_rna_motif)
        sorted_known_specialized = self.alphabetical_sort(known_specialized)
        sorted_comparative = self.alphabetical_sort(comparative)
        sorted_abinitio = self.alphabetical_sort(abinitio)

        predictor.softs_help = known_homology
        predictor.sorted_softs = sorted_known_homology
        predictor.softs_desc = d_known_homology
        self.content.KNOWN_HOMOLOGY_PREDICTORS_LIST = str(predictor)

        predictor.softs_help = known_rna_motif
        predictor.sorted_softs = sorted_known_rna_motif
        predictor.softs_desc = d_known_rna_motif
        self.content.KNOWN_RNA_MOTIF_PREDICTORS_LIST = str(predictor)

        predictor.softs_help = known_specialized
        predictor.sorted_softs = sorted_known_specialized
        predictor.softs_desc = d_known_specialized
        self.content.KNOWN_SPECIALIZED_PREDICTORS_LIST = str(predictor)

        predictor.softs_help = comparative
        predictor.sorted_softs = sorted_comparative
        predictor.softs_desc = d_comparative
        self.content.COMPARATIVE_PIPELINES_LIST = str(predictor)

        predictor.softs_help = abinitio
        predictor.sorted_softs = sorted_abinitio
        predictor.softs_desc = d_abinitio
        self.content.ABINITIO_PREDICTORS_LIST = str(predictor)
        
        self.content.NB_SEQUENCE_LIMITATION = self.model.get_nb_sequence_limitation()
        self.content.SEQUENCE_SIZE_LIMITATION = self.model.get_sequence_size_limitation()

        self.content.SHORT_TABLE_OF_CONTENTS = str(self.toc)
        self.content.mount_point = self.model.get_mount_point()
        self.view.mount_point = self.model.get_mount_point()
        self.view.help = str(self.content)
        return str(self.view)
        
