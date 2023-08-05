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
import time
import re

from rnaspace.core.id_tools import id_tools
from rnaspace.core.exploration.rnaplot import rnaplot
from rnaspace.core.data_manager import data_manager
from rnaspace.core.putative_rna import putative_rna
from rnaspace.core.secondary_structure import secondary_structure
from rnaspace.core.exploration.rnafold import rnafold
from rnaspace.core.trace.event import add_rna_event, edit_rna_event
from rnaspace.core.trace.event import disk_error_event
from rnaspace.core.exceptions import disk_error


class putative_rna_visualisation_model(object):
    """ Class putative_rna_visualisation_model: the model of the putative_rna_visualisation page
    """

    extremity_size = 35
    rna_size_to_display = 100
    ids_max_length = 15
    max_rna_size_for_structure_prediction = 1000
    
    predictors = ["RNAfold"]

    def __init__(self):
        """ Build a putative_rna_visualisation_model object defined by    
            data_manager(type:core.data_manager)   the application data manager  
        """
        self.data_manager = data_manager()
        
    def user_has_data(self, user_id):
        """ Return True if the user has data, false else 
            user_id(type:string)   the user id
        """
        return self.data_manager.user_has_data(user_id)

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

    def get_putative_rna(self, user_id, project_id, params):
        """ Return(putative_rna) the putative_rna defined by its id
            Raise IOError if no putative_rna found 
            user_id(type:string)      the user id
            rna_id(type:string)       the putative_rna id
            project_id(type:string)   project id the user is working on
        """
        if self.get_mode(params) == "creation":
            ids_gen = id_tools()
            current_seq_id = self.get_current_sequence_id(user_id, project_id, params)
            seq = self.data_manager.get_sequence(user_id, current_seq_id, project_id)
            current_rna_id = ids_gen.get_current_putative_rna_id(user_id, project_id, current_seq_id)
            rna = putative_rna(current_rna_id, current_seq_id, 1, 1, "explore", current_rna_id, seq.data[0:1], "unknown", "+", 
                               seq.domain, seq.species, seq.strain, seq.replicon, [], 0.0, "user", "", 
                               str(time.localtime()[2]), str(time.localtime()[1]), str(time.localtime()[0]), [])
        elif self.get_mode(params) == "merge":
            ids_gen        = id_tools()                                                                                               
            rnas_to_merge  = self.get_rnas_to_merge(user_id, project_id, params)
            for rna in rnas_to_merge:
                if rna is None:
                    return None
            current_seq_id = rnas_to_merge[0].genomic_sequence_id
            seq = self.data_manager.get_sequence(user_id, current_seq_id, project_id)
            current_rna_id = ids_gen.get_current_putative_rna_id(user_id, project_id, current_seq_id)

            start     = -1
            stop      = -1
            strand    = "."
            family    = ""         
            predictor = "Merged:"
            for rna in rnas_to_merge:
                if rna.start_position < start or start == -1:
                    start = rna.start_position
                if rna.stop_position > stop:
                    stop = rna.stop_position
                if rna.strand != ".":
                    strand = rna.strand
                if not re.search(rna.family, family):
                    family += rna.family + "/"        
                if re.search("Merged:", rna.program_name):
                    rna.program_name = rna.program_name[7:]
                if not re.search(rna.program_name, predictor):
                    predictor += rna.program_name + "/"
            family = family[:-1]
            predictor = predictor[:-1]
            rna = putative_rna(current_rna_id, current_seq_id, start, stop, "explore", current_rna_id, seq.data[start-1:stop],
                               family, strand, seq.domain, seq.species, seq.strain, seq.replicon, [], 0.0, predictor, "", 
                               str(time.localtime()[2]), str(time.localtime()[1]), str(time.localtime()[0]), [])
        else:
            rna_id = self.__get_rna_id(params) 
            rna = self.data_manager.get_putative_rna(user_id, rna_id, project_id)
            
        return rna

    def update_putative_rna(self, user_id, project_id, rna, seq, params):
        """ Return(putative_rna) the putative_rna defined by its id
            Raise IOError if no putative_rna found 
            user_id(type:string)      the user id
            rna_id(type:string)       the putative_rna id
            project_id(type:string)   project id the user is working on
        """
        
        prna = putative_rna(rna.sys_id, rna.genomic_sequence_id, rna.start_position, rna.stop_position, 
                            rna.run, rna.user_id, rna.sequence, rna.family, rna.strand, rna.domain, 
                            rna.species, rna.strain, rna.replicon, [], rna.score, 
                            rna.program_name, rna.program_version, rna.day, rna.month, rna.year, [])
        
        
        if self.get_action(params) != "cancel_modification" and self.get_action(params) != "":
            for keys in params:
                if keys == "user_rna_id":
                    prna.user_id = params[keys]
                else:
                    prna.set_x(keys, params[keys])
        
        save_strand = prna.strand
        save_start = int(prna.start_position)
        save_end = int(prna.stop_position)
        
        prna.start_position = long(self.__get_new_start(params))
        prna.stop_position = long(self.__get_new_stop(params))
        prna.strand = self.__get_new_strand(params)
        size = int(prna.stop_position) - int(prna.start_position) + 1
    
        prna.sequence = seq.data[int(prna.start_position)-1:int(prna.stop_position)]
    
        if prna.strand == "-":
            prna.sequence = self.__get_reverse_complement(prna.sequence)
                
        prna.structure = self.__get_structures(params)
        new_struct = self.__get_new_structure(params)
        if new_struct != None:
            prna.structure.append(new_struct)
        
            
        alignments = rna.alignment
        align_to_keep = []
        for align_id in alignments:
            align = self.data_manager.get_alignment(user_id, project_id, 
                                                    align_id)
            if align is not None:
                for entry in align.rna_list:
                    if entry.rna_id == rna.sys_id:                    
                        astart = min(entry.start, entry.stop) 
                        astop = max(entry.start, entry.stop) 
                        pstart = min(prna.start_position, prna.stop_position)
                        pstop = max(prna.start_position, prna.stop_position)
                        if astart >= pstart and astop <= pstop:
                            align_to_keep.append(align_id)
                        break

        prna.alignment = align_to_keep

        prna.size = abs(size)
        if save_strand != prna.strand:
            prna.structure = []
        else:
            for struct in range(len(prna.structure)):
                if len(prna.structure[struct].structure) != len(prna.sequence):
                    if (int(prna.start_position) <= save_end and int(prna.start_position) >= save_start) or (int(prna.stop_position) <= save_end and int(prna.stop_position) >= save_start) or (save_start >= int(prna.start_position) and save_start <= int(prna.stop_position) and save_end >= int(prna.start_position) and save_end <= int(prna.stop_position)) :
                        if save_start < int(prna.start_position): 
                            for i in range(int(prna.start_position) - save_start):
                                prna.structure[struct].structure = self.__del_1_begin(prna.structure[struct].structure)
                        if save_start > int(prna.start_position):
                            for i in range(save_start - int(prna.start_position)):
                                prna.structure[struct].structure = self.__add_1_begin(prna.structure[struct].structure)
                        if save_end < int(prna.stop_position):
                            for i in range(int(prna.stop_position) - save_end):           
                                prna.structure[struct].structure = self.__add_1_end(prna.structure[struct].structure)
                        if save_end > int(prna.stop_position):
                            for i in range(save_end - int(prna.stop_position)):                     
                                prna.structure[struct].structure = self.__del_1_end(prna.structure[struct].structure)
                    else:
                        prna.structure[struct].structure = ""
                        for i in prna.sequence:
                            prna.structure[struct].structure += "."
        return prna

    def save_putative_rna(self, user_id, project_id, params):
        rna = self.get_putative_rna(user_id, project_id, params)
        old_alignments = rna.alignment
        sequence = self.get_sequence(user_id, project_id, rna, params)
        updated_rna = self.update_putative_rna(user_id, project_id, rna, sequence, params)
        alignments_to_delete = []
                
        for align in old_alignments:
            if align not in updated_rna.alignment:
                alignments_to_delete.append(align)
            
        try:
            self.data_manager.update_putative_rna(user_id, project_id,
                                                  rna.sys_id, updated_rna)
            for align in alignments_to_delete:
                self.data_manager.delete_alignment(user_id, project_id, align)

        except disk_error, e:
            mail = self.data_manager.get_user_email(user_id, project_id)
            project_size = self.data_manager.get_project_used_space(user_id,
                                                                    project_id)
            ev = disk_error_event(user_id, project_id, mail, e.message,
                                  project_size)
            
            self.data_manager.update_project_trace(user_id, project_id, [ev])
            raise


        if len(alignments_to_delete)!=0:
            modified_nb_alignment = 0
        else:
            modified_nb_alignment = None
        if rna.user_id != updated_rna.user_id:
            modified_rna_user_id = updated_rna.user_id
        else:
            modified_rna_user_id = None
        if rna.sequence != updated_rna.sequence:
            modified_rna_sequence = updated_rna.sequence
        else: 
            modified_rna_sequence = None
        if rna.family != updated_rna.family:
            modified_rna_family = updated_rna.family
        else: 
            modified_rna_family = None
        if str(rna.start_position) != str(updated_rna.start_position):
            modified_start_position = updated_rna.start_position
        else: 
            modified_start_position = None
        if str(rna.stop_position) != str(updated_rna.stop_position):
            modified_stop_position = updated_rna.stop_position
        else: 
            modified_stop_position = None
        if rna.strand != updated_rna.strand:
            modified_strand = updated_rna.strand
        else: 
            modified_strand = None
        if len(rna.structure) != len(updated_rna.structure):
             modified_structure = updated_rna.structure
        else:
            modified_structure = None
            for i in range(0,len(rna.structure)):
                if rna.structure[i].structure != updated_rna.structure[i].structure:
                    modified_structure = updated_rna.structure
        
        e = edit_rna_event(user_id, project_id,
                           self.data_manager.get_user_email(user_id,project_id),
                           updated_rna.user_id,
                           rna_user_id=modified_rna_user_id, seq_name=modified_rna_sequence,
                           family=modified_rna_family, start=modified_start_position, 
                           stop=modified_stop_position, strand=modified_strand,
                           secondary_structures=modified_structure, nb_alignment=modified_nb_alignment)
        self.data_manager.update_project_trace(user_id,project_id, [e])


    def add_putative_rna(self, user_id, project_id, params):
        rna = self.get_putative_rna(user_id, project_id, params)
        sequence = self.get_sequence(user_id, project_id, rna, params)
        rna = self.update_putative_rna(user_id, project_id, rna, sequence, params)
        ids_gen = id_tools()
        ids_gen.get_new_putativerna_id(user_id, project_id, sequence.id)
        prnas_to_add = []
        prnas_to_add.append(rna)

        try:
            self.data_manager.add_putative_rnas(user_id, project_id,
                                                prnas_to_add)
        except disk_error, e:
            mail = self.data_manager.get_user_email(user_id, project_id)
            project_size = self.data_manager.get_project_used_space(user_id,
                                                                    project_id)
            ev = disk_error_event(user_id, project_id, mail, e.message,
                                  project_size)
            
            self.data_manager.update_project_trace(user_id, project_id, [ev])
            raise

        
        #If merged
        rnas_to_merged = self.get_rnas_to_merge(user_id, project_id, params)
        align_to_delete = []
        for prna in rnas_to_merged:
            align_to_delete.extend(prna.alignment)
        for align in align_to_delete:
            self.data_manager.delete_alignment(user_id, project_id, align)
        rnas_to_merged_id = []
        for rna_merge in rnas_to_merged:
            rnas_to_merged_id.append(rna_merge.sys_id)        
        self.data_manager.delete_putative_rnas(user_id, project_id, rnas_to_merged_id)
        if self.get_action(params) == "merged":
            pass
        else:
            e = add_rna_event(user_id, project_id,
                               self.data_manager.get_user_email(user_id,project_id),
                               rna.user_id,
                               seq_name=rna.sequence,
                               family=rna.family, start=rna.start_position, 
                               stop=rna.stop_position, strand=rna.strand,
                               secondary_structures=rna.structure, nb_alignment=0)
            self.data_manager.update_project_trace(user_id,project_id, [e])
        return rna.sys_id

    def get_mode(self, params):
        """ Return the mode from params
            params(type:{})     the dictionary of parameters
        """
        if params.has_key("mode"):
            return params["mode"]
        else:
            return "display"

    def get_genomical_context(self, seq, rna):
        """ Return a table of sequence the view has to display [before_seq, after_seq]
            user_id(type:string)      the user id
            project_id(type:string)   project id the user is working on
            params(type:{})         the dictionary of parameters
        """
        begin = int(rna.start_position)
        end = int(rna.stop_position)
        try:
            if begin < 0:
                begin = 0
            if end > len(seq.data):
                end = len(seq.data)
            
            if begin - self.extremity_size < 0:
                before_seq = seq.data[0:begin-1]
                if rna.strand == "-":
                    before_seq = self.__get_reverse_complement(before_seq)
            else:
                before_seq = seq.data[begin-self.extremity_size-1:begin-1]
                if rna.strand == "-":                  
                    before_seq = self.__get_reverse_complement(before_seq)

            if end + self.extremity_size > len(seq.data):
                after_seq = seq.data[end:len(seq.data)]
                if rna.strand == "-":
                    after_seq = self.__get_reverse_complement(after_seq)                                    
            else:
                after_seq = seq.data[end:end + self.extremity_size]
                if rna.strand == "-":
                    after_seq = self.__get_reverse_complement(after_seq)                                         

            sequences = []
            if rna.strand == "-":
                sequences.append(after_seq)
                sequences.append(before_seq)
            else:
                sequences.append(before_seq)
                sequences.append(after_seq)
            return sequences
        except:
            raise IOError

    def get_current_sequence_id(self, user_id, project_id, params):
        """ Return the current sequence id
            user_id(type:string)      the user id
            project_id(type:string)   project id the user is working on
            params(type:{})         the dictionary of parameters
        """
        if params.has_key("current_sequence_id"):
            return params["current_sequence_id"]
        else:
            tab = self.get_sequences_id(user_id, project_id, params)
            return tab[0]

    def get_error_msg(self, params):
        if params.has_key("error"):
            return params["error"]
        else:
            return ""

    def get_sequences_id(self, user_id, project_id, params):
        """ Return a table of sequences id linked to the given project
            user_id(type:string)      the user id
            project_id(type:string)   project id the user is working on
            params(type:{})         the dictionary of parameters
        """
        if self.get_mode(params) == "creation":
            return self.data_manager.get_sequences_id(user_id, project_id)
        else:
            rna = self.get_putative_rna(user_id, project_id, params)
            res = []
            res.append(rna.genomic_sequence_id)
            return res

    def get_structures_picture(self, user_id, project_id, rna):
        """ Return([string]) a table with the structures picture path
            user_id(type:string)      the user id
            project_id(type:string)   project id the user is working on
            rna(type:putative_rna)    the putative_rna
        """
        paths = []
        drawer = rnaplot()
        output = self.data_manager.config.get("storage", "tmp_dir")

        for struct in rna.structure:
            paths.append(drawer.run(user_id, project_id, rna.sequence, struct, output))
        return paths

    def get_structure_picture_content(self, name):
        tmp_dir = self.data_manager.config.get("storage", "tmp_dir")
        path = os.path.join(tmp_dir, name)

        # protect the reading of other than image files in tmp_dir
        if os.path.dirname(path) != tmp_dir:
            return "Sorry, this file is not an image..."
        fpath = open(path, 'r')
        return fpath

    def get_new_structure(self, rna, params, user_id, project_id):
        if self.get_action(params) == "predict":
            if self.__get_predictor(params) == "RNAfold":
                predictor = rnafold()
            else:
                predictor = rnafold()
            structure = predictor.run(rna.sequence, user_id, project_id)
        else:
            str_value = ""
            for i in rna.sequence:
                str_value += "."
            structure = secondary_structure("brackets", str_value, "user", 0.0)
        return structure
    
    def get_sequence(self, user_id, project_id, rna, params):
        if self.get_mode(params) == "creation":
            seq_id = self.get_current_sequence_id(user_id, project_id, params)
        else:
            seq_id = rna.genomic_sequence_id
        seq = self.data_manager.get_sequence(user_id, seq_id, project_id)
        return seq
    
    def get_rna_names_already_used(self, user_id, project_id):
        rnas = self.data_manager.get_putative_rnas(user_id, project_id)
        names = ""
        for rna in rnas:
            names += rna.user_id + ","
        return names[:len(names)-1]
    
    def get_action(self, params):
        """ Return the action from params
            params(type:{})     the dictionary of parameters
        """
        if params.has_key("action"):
            return params["action"]
        else:
            return ""

    def get_rnas_to_merge(self, user_id, project_id, params):
        """ Return a dictionary of putative_rna indexed by their sys_id
            user_id(type:string)      the user id
            project_id(type:string)   project id the user is working on
            params(type:{})         the dictionary of all the parameters
        """
        result_table = []
        if params.has_key("nb_putative_rnas"):
            for i in range(int(params["nb_putative_rnas"])):
                param_name = "putative_rna" + str(i)
                result_table.append(self.data_manager.get_putative_rna(user_id, params[param_name], project_id))
        return result_table
    
    def __get_predictor(self, params):
        """ Return the predictor from params
            params(type:{})     the dictionary of parameters
        """
        if params.has_key("predictor"):
            return params["predictor"]
        else:
            return ""

    def __get_rna_id(self, params):
        """ Return the rna_id from params
            params(type:{})     the dictionary of parameters
        """
        if params.has_key("rna_id"):
            return params["rna_id"]
        else:
            return None

    def __get_new_start(self, params):
        """ Return the rna_id from params
            params(type:{})     the dictionary of parameters
        """
        if params.has_key("start_position_value"):
            return params["start_position_value"]
        else:
            return 1
        
    def __get_new_stop(self, params):
        """ Return the rna_id from params
            params(type:{})     the dictionary of parameters
        """
        if params.has_key("stop_position_value"):
            return params["stop_position_value"]
        else:
            return 1

    def __get_new_strand(self, params):
        """ Return the rna_id from params
            params(type:{})     the dictionary of parameters
        """
        if params.has_key("strand_value"):
            return params["strand_value"]
        else:
            return "+"
        
    def __get_complement(self, base):
        """ Return the complement base
            base(string)     the base to complement
        """
        cbase_table = {
            'A': 'T',
            'a': 't',
            'T': 'A',
            't': 'a',
            'C': 'G',
            'c': 'g',
            'G': 'C',
            'g': 'c',
            'N': 'N',
            'n': 'n',
            'U': 'A',
            'u': 'a'}
        return cbase_table[base]
 
    def __get_reverse_complement(self, seq):
        """ Return the reverse complement sequence
            seq(string)     the sequence to reverse and complement
        """
        rc_seq = ""
        for base in reversed(seq):
            rc_seq += self.__get_complement(base)
        return rc_seq

    def __parse_structure(self, str):
        """ Return the structure parsed into a table
            str(string)     the structure to parse
        """
        result = []
        for i in range(len(str)):
            result.append("")
        p = []
        for i in range(len(str)):
            if str[i] == "(":
                p.append(i)
            elif str[i] == ".":
                result[i] = -1
            else:
                if len(p) == 0:
                    return -1
                j = p.pop()
                result[i] = j
                result[j] = i
        if len(p) != 0:
            return -1
        else: return result

    def __add_1_begin(self, str):
        """ Add 1 '.' to the structure
            str(string)     the structure to modify
        """
        return "." + str
    
    def __add_1_end(self, str):
        """ Add 1 '.' to the end of the structure
            str(string)     the structure to modify
        """
        return str + "."
    
    def __del_1_begin(self, str):
        """ delete the first value of the structure and replace by a dote the linked
            parenthesis if necessary
            str(string)     the structure to modify
        """
        if str[0] == ".":
            return str[1:len(str)]
        else:
            tab = self.__parse_structure(str)
            str = str[0:tab[0]] + "." + str[tab[0]+1:len(str)]
            return str[1:len(str)]

    def __del_1_end(self, str):
        """ delete the last value of the structure and replace by a dote the linked
            parenthesis if necessary
            str(string)     the structure to modify
        """
        if str[len(str)-1] == ".":
            return str[0:len(str)-1]
        else:
            tab = self.__parse_structure(str)
            str = str[0:tab[len(str)-1]] + "." + str[tab[len(str)-1]+1:len(str)]
            return str[0:len(str)-1]

    def __get_new_structure(self, params):
        if self.get_action(params) == "addstructure":
            ss = secondary_structure("brakets", params["new_structure"], params["new_structure_predictor"], params["new_structure_fenergy"])
            return ss
        else:
            return None
    
    def __get_structures(self, params):
        structs = []
        for i in range(int(params["nb_structures"])):
            if not(self.get_action(params) == "delstructure" and i == int(params["structure_to_delete"])):
                structs.append(secondary_structure("brakets", params["structure"+str(i)], params["structure_predictor"+str(i)], params["structure_fenergy"+str(i)]))
        return structs
    
    def __get_alignments(self, params):
        aligns = []
        try:
            for i in range(int(params["nb_alignments"])):
                if not(self.get_action(params) == "delalignment" and i == int(params["alignment_to_delete"])):
                    aligns.append(params["alignment"+str(i)])
        except:
            pass
        return aligns


    def get_mount_point(self):
        return self.data_manager.get_mount_point()
