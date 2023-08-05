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
import tempfile
import StringIO
import re

from rnaspace.core.exceptions import disk_error
from rnaspace.core.data_manager import data_manager
from rnaspace.core.id_tools import id_tools
from rnaspace.core.sequence import sequence
from rnaspace.core.trace.event import add_seq_event
from rnaspace.core.trace.event import disk_error_event
import rnaspace.core.common as common_core

class manage_model(object):
    """ Class manage_model: the model of the manage page
    """

    available_domain = ["bacteria", "eukaryote", "archaea"]

    def __init__(self):
        """ Build a manage_model object defined by    
            data_manager(type:core.data_manager)   the application data manager  
        """
        self.data_manager = data_manager()
        
    def add_sequences(self, user_id, project_id, params):
        """
        Save the user sequences return 1 if everything ok, 0 otherwise.

        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        fseq(file object)     the sequence we want to save
        params({})            the infos of the sequence
        """

        fseq = self.__get_sequences(params)
        if not self.__valid_fasta_sequence(fseq):
            raise ImportError, 'Sequence in wrong fasta format'
        
        fseq.seek(0)

        id = self.__get_seq_id(params)
        id_t = id_tools()
        if id == id_t.get_current_sequence_id(user_id, project_id):
            id = id_t.get_new_sequence_id(user_id, project_id)
        domain = self.__get_domain(params)
        species = self.__get_species(params)
        strain = self.__get_strain(params)
        replicon = self.__get_replicon(params)
        
        seq_data = ''
        i = 1
        seqs = []
        for line in fseq:
            if line.startswith('>'):
                if len(seqs) >= self.data_manager.get_nb_sequences_limitation() - 1:
                    raise ImportError, 'Too many sequences into your fasta file ! Maximum allowed is '  + str(self.data_manager.get_nb_sequences_limitation()) + ' per fasta file.'
                else:
                    if seq_data != '':
                        tmp_id = id + "." + str(i)
                        seq = sequence(tmp_id, seq_data, domain, species, replicon, strain)
                        seqs.append(seq)
                        i = i + 1
                    seq_data = line.replace('\r', '')
            else:
                temp = line.upper()
                temp = temp.replace('\r', '')
                seq_data += temp
        if i != 1:
            tmp_id = id + "." + str(i)
        else:
            tmp_id = id
        seq = sequence(tmp_id, seq_data, domain, species, replicon, strain)
        seqs.append(seq)
        
        for seq in seqs:
            try:
                self.add_sequence(user_id, project_id, seq)
            except disk_error, e:
                project_size = self.data_manager.get_project_used_space(user_id,
                                                                        project_id)
                ev = disk_error_event(user_id, project_id, "-", e.message,
                                      project_size)
                self.data_manager.update_project_trace(user_id, project_id, [ev])
                raise
        
        fseq.close()
        
    def add_sequence(self, user_id, project_id, seq):
        
        max_length = self.data_manager.get_sequence_size_limitation()
        current_size = self.data_manager.get_user_sequences_used_space(user_id, project_id)
        if len(seq.data) + current_size < max_length:
            self.data_manager.add_sequence(user_id, project_id, seq)

            e = add_seq_event(user_id, project_id,
                              "-",
                              seq.id,
                              len(seq.data),
                              self.data_manager.get_sequence_header(user_id, project_id, seq.id),
                              0)
            self.data_manager.update_project_trace(user_id,project_id, [e])

        else:
            space_left = max_length - current_size
            if space_left < 0:
                space_left = 0
            raise ImportError, 'Sequence length is way too long! You have '  + common_core.get_octet_string_representation(space_left) + ' left to import sequence(s)!'

    def get_sequence_size_limitation(self):
        return common_core.get_octet_string_representation(self.data_manager.get_sequence_size_limitation())

    def get_nb_sequences_limitation(self):
        return self.data_manager.get_nb_sequences_limitation()

    def create_new_project(self, user_id):
        """
        Return                the user projects' id
        user_id(string)       the id of the connected user
        """
        return self.data_manager.new_project(user_id)
    
    def get_sample_sequence(self, params):
        if self.__get_sample_sequence(params) == "True":
            current_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(current_dir, "../../ressource/sample/")
            file = os.path.join(path, "sample.fna")
            infos_path = os.path.join(path, "sample.txt")
            data = ""
            for ligne in open(file):
                data += ligne
        
            infos_file = open(infos_path, 'r')
            infos = infos_file.read().split('\n')
            infos_dict = {}
            for line in infos:
                info = line.split('=')
                infos_dict[info[0]] = info[1]

            infos_file.close()
            seq = sequence("sample", data, 
                           domain=infos_dict['domain'],
                           replicon=infos_dict['replicon'],
                           species=infos_dict['species'], 
                           strain=infos_dict['strain'])
            return seq
        else:
            return None 
    
    def get_current_sequence_id(self, user_id, project_id):
        """
        Return                the current sequence id
        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        """    
        id_t = id_tools()
        return id_t.get_current_sequence_id(user_id, project_id)

    def save_user_email(self, user_id, project_id, params):
        """
        Save the user email
        user_id(string)          the id of the connected user
        email(string)            the email address
        project_id(string)       the project id
        params({})               the page params
        """
        email = self.__get_user_email(params)
        self.data_manager.save_user_email(user_id, project_id, email)

        
    def get_project_sequences(self, user_id, project_id):
        """
        Return                the sequence ids the project
        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        """
        sequences = []        
        try:
            ids = self.data_manager.get_sequences_id(user_id, project_id)   
            for id in sorted(ids):
                sequences.append(self.data_manager.get_sequence(user_id, id, project_id))
        except:
            pass
        return sequences

    def get_putative_rnas(self, user_id, project_id):
        """
        Return(string)        table of putative rnas
        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        """        
        prnas = {}
        try:
            prnas = self.data_manager.get_putative_rnas_by_runs(user_id, project_id)
        except:
            pass
        return prnas
        
    def get_alignments(self, user_id, project_id):
        return self.data_manager.get_alignments(user_id, project_id)
    
    def delete_alignment(self, user_id, project_id, params):
        align_id = self.__get_alignment_to_delete(params)
        if align_id != None:
            self.data_manager.delete_alignment(user_id, project_id, align_id)
    
    def delete_run(self, user_id, project_id, params):
        run_id = self.__get_run_to_delete(params)
        if run_id != None:
            self.data_manager.delete_run(user_id, project_id, run_id)
    
    def get_error_msg(self, params):
        if params.has_key("error"):
            return params["error"]
        else:
            return ""
    
    def get_project_sequences_header(self, user_id, project_id):
        """
        Return(string)        the header of the project sequences
        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        """
        headers = {}
        try:
            ids = self.data_manager.get_sequences_id(user_id, project_id)
            for id in ids:
                headers[id] = self.data_manager.get_sequence_header(user_id, project_id, id)
        except:
            pass
        return headers

    def is_an_authentification_platform(self):
        return self.data_manager.is_an_authentification_platform()
    
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

    def get_action(self, params):
        if params.has_key("action"):
            return params["action"]
        else:
            return None

    def get_unknown_user_name(self):
        return self.data_manager.get_unknown_user_name()

    def __get_user_email(self, params):
        if params.has_key("email"):
            return params["email"]
        else:
            return ""

    def __get_sample_sequence(self, params):
        if params.has_key("get_sample_sequence"):
            return params["get_sample_sequence"]
        else:
            return "False"

    def __valid_fasta_sequence(self, fseq):
        """        
        check the validity of the fasta file
        Return(boolean)       Tue if the sequence is in fasta format,
                              False otherwise
        fseq(file object)     the sequence we want to check
        """
        pattern = "^(>.+[\r\n]+)([ATCGUNatcgun\ ]+[\r\n]+)+"
        oneseq_pattern = re.compile(pattern)
        seq = ''
        i = 0
        for line in fseq:
            if line.startswith('>'):
                if seq != '':
                    if not oneseq_pattern.search(seq):
                        return False
                    i = i + 1
                seq = line
            else:
                seq += line
        if not oneseq_pattern.search(seq + '\n'):
            return False
        return True

    def __get_domain(self, params):
        if params.has_key("domain"):
            return params["domain"]
        else:
            return "unknown"
        
    def __get_species(self, params):
        if params.has_key("species"):
            return params["species"]
        else:
            return "unknown"
        
    def __get_strain(self, params):
        if params.has_key("strain"):
            return params["strain"]
        else:
            return "unknown"
        
    def __get_replicon(self, params):
        if params.has_key("replicon"):
            return params["replicon"]
        else:
            return "unknown"
        
    def __get_seq_id(self, params):
        if params.has_key("id"):
            return params["id"]
        else:
            return "unknown"

    def __get_alignment_to_delete(self, params):
        if params.has_key("alignment_to_delete"):
            return params["alignment_to_delete"]
        else:
            return None

    def __get_run_to_delete(self, params):
        if params.has_key("run_to_delete"):
            return params["run_to_delete"]
        else:
            return None
    
    def __get_sequences(self, params):
        abs_path = ''
        if self.__is_file_to_upload(params):
            os_temp, abs_path = tempfile.mkstemp()
            temp = open(abs_path, 'a')
            # avoid huge use of memory
            while True:
                data = params['file'].file.read(8192)
                if not data:
                    break
                temp.write(data)            
            temp.close()
            fseq = open(abs_path, 'r')
        else:
            seq = params['sequences']
            # get a file-object from the string seq
            fseq = StringIO.StringIO(seq)
        return fseq

    def __is_file_to_upload(self, params):
        if params.has_key("sequences"):
            if params["sequences"] == "":
                return True
            else:
                return False
        else:
            return False
    
    def get_mount_point(self):
        return self.data_manager.get_mount_point()
