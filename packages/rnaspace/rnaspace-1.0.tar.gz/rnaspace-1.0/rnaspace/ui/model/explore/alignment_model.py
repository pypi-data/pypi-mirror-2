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

import time
import re
import os
from StringIO import StringIO

from rnaspace.core.data_manager import data_manager
from rnaspace.core.trace.event import align_event, add_alignment_event, alignment_error_event
from rnaspace.core.exploration.rnaplot import rnaplot
from rnaspace.core.exploration.aligner_manager import aligner_manager
import rnaspace.core.exploration.color_sequences as color_sequences
from rnaspace.core.exceptions import disk_error
from rnaspace.core.email_sender import email_sender

class alignment_model(object):
    """ Class allignement_model: the model of the allignement page
    """

    aligners = ["rnaz_aligner"]
    max_item_length = 14
    
    def __init__(self):
        """ 
        Build an allignement_model object defined by    
        data_manager(type:core.data_manager)   the application data manager  
        """
        self.data_manager = data_manager()
        self.aligner_manager = aligner_manager()
        self.aligner = alignment_model.aligners
        self.email_s = email_sender()

    def user_has_data(self, user_id):
        """ 
        Return True if the user has data, false else 
        user_id(type:string)   the user id
        """
        return self.data_manager.user_has_data(user_id)

    def get_mode(self, params):
        """
        Return the mode for alignment: can be "display"
        """
        if params.has_key("mode"):
            return params["mode"]
        else:
            return ""

    def get_action(self, params):
        if params.has_key("action"):
            return params["action"]
        else:
            return ""

    def get_prnas_ids(self, params):
        return self.__get_putative_rnas(params)

    def get_alignments_ids(self, params):
        selected = []
        if params.has_key("nb_alignments"):
            for i in range(int(params["nb_alignments"])):
                name = "alignment" + str(i)
                if params.has_key(name):
                    selected.append(params[name])
        elif params.has_key("alignment_id"):
            selected.append(params["alignment_id"])
        return selected

    def get_alignments_ids_for_prna(self, user_id, project_id, prna_id):
        prna = self.data_manager.get_putative_rna(user_id, prna_id, project_id)
        align_ids = []
        for align_id in prna.alignment:
            align_ids.append(align_id)
        return align_ids

    def get_colored_alignments(self, user_id, project_id, align_ids, 
                               mount_point):
        blocks = {}

        aligns = self.get_alignments(user_id, project_id, align_ids)

        for align in aligns: 

            prnas = []
            fasta = ""
            has_struct = True
            if align is None:
                continue
            
            for prna in align.rna_list:
                if not prna.rna_id.startswith("%"):
                    fasta += '>' + prna.user_id + '\n'
                    fasta += prna.sequence + '\n'
                    if prna.structure is not None:
                        fasta += prna.structure.structure + '\n'
                    else:
                        has_struct = False
            for prna in align.rna_list:
                if prna.rna_id.startswith("%"):
                    fasta += '>' + prna.user_id + '\n'
                    fasta += prna.sequence + '\n'
                    if prna.structure is not None:
                        fasta += prna.structure.structure + '\n'

            if align.consensus is not None:
                fasta += '>consensus\n'
                fasta += align.consensus.sequence + '\n'
                if len(align.consensus.structure)>0 and has_struct:
                    fasta += align.consensus.structure[0].structure + '\n'

            rna_m = color_sequences.get_color(StringIO(fasta))

            if has_struct:
                rna_m.compute_super()
                rna_m.compute_color()
            rna_m.compute_comment()
            fhtml = StringIO()

            for prna in align.rna_list:

                uprna = self.data_manager.get_putative_rna(user_id, 
                                                           prna.rna_id, 
                                                           project_id)

                if uprna is not None:
                    prnas.append(uprna)

                for rna in rna_m.sequences:
                    if (rna.user_name == prna.user_id or 
                        '%>' + rna.user_name[1:] == prna.user_id):
                        if uprna is not None:
                            if prna.strand == "+" or prna.strand == ".":
                                rna.begin = prna.start - uprna.start_position + 1
                                rna.end  = prna.stop - uprna.start_position + 1
                            else:
                                rna.begin = prna.stop - uprna.start_position + 1
                                rna.end  = prna.start - uprna.start_position + 1
                        else:
                            if prna.strand == "+" or prna.strand == ".":
                                rna.begin = prna.start
                                rna.end  = prna.stop
                            else:
                                rna.begin = prna.stop
                                rna.end  = prna.start

            img_url = None        
            if align.consensus is not None and len(align.consensus.structure)>0:
                drawer = rnaplot()
                output = self.data_manager.config.get("storage", "tmp_dir")

                try:
                    authkey = self.data_manager.get_authkey(user_id, project_id)
                    img_path = drawer.run(user_id, project_id, align.consensus.sequence, 
                                          align.consensus.structure[0], output)
                    img_url = mount_point  
                    img_url += 'explore/alignment/picture?name=%s&amp;authkey=%s'
                    img_url = img_url % (img_path, authkey)
                except:
                    img_url = None

            saved = True
            if align.id.startswith("tmp_"):
                saved = False
            blocks[align.id] = {"rnas":rna_m, 
                                "program":align.program_name,
                                "consensus":img_url,
                                "saved":saved,
                                "entries":align.rna_list,
                                "score":align.score,
                                "evalue":align.evalue,
                                "pvalue":align.pvalue,
                                "prnas":prnas
                                }
            fhtml.close()
        return blocks

    def get_structure_picture_content(self, name):
        tmp_dir = self.data_manager.config.get("storage", "tmp_dir")
        path = os.path.join(tmp_dir, name)

        # protect the reading of other than image files in tmp_dir
        if os.path.dirname(path) != tmp_dir:
            return "Sorry, this file is not an image..."

        fpath = open(path, 'r')
        return fpath

    def get_alignments(self, user_id, project_id, align_ids):
        aligns = []
        for align_id in align_ids:
            if re.search("^tmp_", align_id):
                align = self.data_manager.get_temporary_alignment(user_id, 
                                                                  project_id, 
                                                                  align_id)
            else:
                align = self.data_manager.get_alignment(user_id, project_id, 
                                                        align_id)
            aligns.append(align)

        return aligns

    def save_alignments(self, user_id, project_id, params):
        alignments = []
        align_ids = [self.__get_alignment_to_save(params)]
        for align_id in align_ids:
            if align_id != -1:
                align = self.data_manager.get_temporary_alignment(user_id, 
                                                                  project_id, 
                                                                  align_id)
                align.id = align.id.split('_')[-1]
                
                try:
                    self.data_manager.add_alignments(user_id, project_id,
                                                     [align])
                except disk_error, e:
                    mail = self.data_manager.get_user_email(user_id, project_id)
                    ev = alignment_error_event(user_id, project_id, mail,
                                               e.__str__(), align.program_name)
                    self.data_manager.update_project_trace(user_id, project_id,
                                                           [ev])
                    raise
                    
                for entry in align.rna_list:                    
                    prna_id = entry.rna_id
                    p = self.data_manager.get_putative_rna(user_id, 
                                                           prna_id, 
                                                           project_id)
                    p.alignment.append(align.id)
                    self.data_manager.update_putative_rna(user_id, project_id, 
                                                          p.sys_id, p)
                alignments.append(align.id)

                rna_user_ids = []
                for entry in align.rna_list:
                    rna_user_ids.append(entry.user_id)
                e = add_alignment_event(user_id, project_id,
                                        self.data_manager.get_user_email(user_id,project_id), rna_user_ids)
                self.data_manager.update_project_trace(user_id, project_id, [e])
        return alignments

    def get_putative_rnas(self, user_id, project_id, params):
        """
        decode params and return the putative_rnas contained in params
        """
        prnas_id = self.__get_putative_rnas(params)
        prnas = []
        for prna_id in prnas_id:
            prna = self.data_manager.get_putative_rna(user_id, prna_id, 
                                                      project_id)
            prnas.append(prna)
        return prnas

    def has_aligner_finished(self, user_id, project_id, params):
        """
        return True if the aligner has finished, False otherwise
        """
        prnas_id = self.__get_putative_rnas(params)
        return self.aligner_manager.has_aligner_finished(user_id, project_id,
                                                         prnas_id)

    def align_putative_rnas(self, user_id, project_id, params):
        """
        Align the putative rnas contained in params
        Return True if aligner is launched successfully, False otherwise
        """
        prnas_id = self.__get_putative_rnas(params)
        t1 = time.clock()
        for aligner in self.aligners:
            align = self.aligner_manager.run_aligner(user_id, project_id, 
                                                     aligner, prnas_id)
        t2 = time.clock()
        e = align_event(user_id, project_id,
                        self.data_manager.get_user_email(user_id,project_id),
                        prnas_id, aligner, t2-t1,
                        self.data_manager.get_project_size(user_id,project_id))
        self.data_manager.update_project_trace(user_id,project_id, [e])
        return align

    def get_aligner_returned_value(self, user_id, project_id, params):
        """
        return the alignments ids generated by aligners
        """
        prnas_id = self.__get_putative_rnas(params)
        align_ids = []
        for aligner in self.aligners:
            align = self.aligner_manager.get_aligner_returned_value(user_id, 
                                                                    project_id, 
                                                                    prnas_id,
                                                                    aligner)
            try:
                align.id
            except:
                return False
            
            align.id = "tmp_" + project_id + '_' + align.id
            self.data_manager.save_alignment_as_temporary(user_id, project_id, 
                                                          align)
            align_ids.append(align.id)

        return align_ids

    def __get_putative_rnas(self, params):
        selected = []
        if params.has_key("nb_putative_rna"):
            for i in range(int(params["nb_putative_rna"])):
                name = "putative_rna" + str(i)
                if params.has_key(name):
                    selected.append(params[name])
        return selected

    def __get_alignment_to_save(self, params):
        if params.has_key("alignment_to_save"):
            return params["alignment_to_save"]
        else:
            return -1

    def is_an_authentification_platform(self):
        return self.data_manager.is_an_authentification_platform()

    def has_user_done_a_run(self, user_id, project_id):
        """
        Return                True if the user has done a run yet, False otherwise
        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        """
        try:
            return self.data_manager.user_has_done_a_run(user_id, project_id)
        except:
            return False

    def get_ids_from_authkey(self, id):
        """
        id(sting)      the id containing the user_id and the project_id
        return [user_id, project_id]
        """
        return self.data_manager.get_ids_from_authkey(id)

    def get_authkey(self, user_id, project_id):
        """
        user_id(sting)      the user_id
        project_id(string)  the project_id
        return the id
        """
        return self.data_manager.get_authkey(user_id, project_id)


    def can_align(self, user_id, project_id, params):
        prnas = self.get_putative_rnas(user_id, project_id, params)
        min_size = prnas[0].size
        max_size = prnas[0].size

        for prna in prnas[1:]:
            max_size = max(max_size, prna.size)
            min_size = min(min_size, prna.size)

        if max_size - min_size > min_size/4:             
            return False
        else:
            return True

    def get_mount_point(self):
        return self.data_manager.get_mount_point()
