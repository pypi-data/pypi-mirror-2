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

import tempfile
import os
import logging

from rnaspace.core.conversion.rnaml import rnaml
from rnaspace.core.conversion.fasta_converter import fasta_converter
from rnaspace.core.conversion.gff_converter import gff_converter
from rnaspace.core.conversion.apollo_gff_converter import apollo_gff_converter
from rnaspace.core.sequence_combiner import sequence_combiner
import rnaspace.core.common as common

from rnaspace.dao.storage_configuration_reader import storage_configuration_reader
from rnaspace.dao.rnaml_putative_rna_handler import rnaml_putative_rna_handler
from rnaspace.dao.dump_putative_rna_handler import dump_putative_rna_handler
from rnaspace.dao.sequence_handler import sequence_handler
from rnaspace.dao.user_handler import user_handler
from rnaspace.dao.predictors_handler import predictors_handler
from rnaspace.dao.rnaml_alignment_handler import rnaml_alignment_handler
from rnaspace.dao.dump_alignment_handler import dump_alignment_handler
from rnaspace.dao.genome_handler import genome_handler
from rnaspace.dao.database_handler import database_handler
from rnaspace.dao.trace_handler import trace_handler

class data_manager(object):
    """ 
    Class data_manager: the data manager is the central point to access to all 
    the plateform data
    """
    
    # list of storage mode available
    available_mode = ["rnaml", "dump"]

    # Singleton
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(data_manager, cls).__new__(cls, *args,
                                                              **kwargs)
        return cls.__instance

    def __init__(self):
        """ 
        Build a data_manager object defined by 
        mode(type:string)                           the storage mode to use
        config(type:storage_configuration_reader)   the config file object   
        putative_rna_handler(putative_rna_handler)  the handler for
                                                    putative_rna objects
        """
        self.config = storage_configuration_reader()

        # get the storage mode from the config file
        self.mode = self.config.get_storage_mode()
        if self.mode in data_manager.available_mode:
            if self.mode == "rnaml":
                self.putative_rna_handler = rnaml_putative_rna_handler()
                self.align_handler = rnaml_alignment_handler()
            elif self.mode == "dump":
                self.putative_rna_handler = dump_putative_rna_handler()
                self.align_handler = dump_alignment_handler()
        else: 
            raise TypeError(self.mode + " found in the rnaspace configuration" +
                        " file is not a valid mode. Please choose in" +
                        " the following available mode: " +
                        str(data_manager.available_mode))
        self.seq_handler = sequence_handler()
        self.user_handler = user_handler()
        self.predic_handler = predictors_handler()
        self.genome_handler = genome_handler()
        self.db_handler = database_handler()
        self.trace_handler = trace_handler()


    def get_mount_point(self):
        return self.config.get("global", "mount_point")

    def get_predictors_conf_directory(self):
        """
        Return(type:string)       directory of predictors configuration files

        """
        return self.config.get_predictors_conf_directory()

    def is_an_authentification_platform(self):
        return self.config.get("global", "authentification_platform") == "true"

    def get_smtpserver(self):
        """
        Return(type:string)      the address of the smtp server
        """
        return self.config.get_smtpserver()

    def get_smtpserver_port(self):
        return self.config.get_smtpserver_port()
        
    def get_smtpserver_login(self):
        return self.config.get_smtpserver_login()

    def get_smtpserver_password(self):
        return self.config.get_smtpserver_password()

    def get_smtp_from_email(self):
        return self.config.get_smtp_from_email()

    def get_admin_email(self):
        return self.config.get_admin_email()
        
    ############################################################################
    ## PUTATIVE RNA FUNCTIONS
    ##

    def get_putative_rna_path(self, user_id, project_id, run_id, p_rna_id):
        """
        Return(type:string)       path to the putative RNA dir

        user_id(type:string)      id of the connected user
        project_id(type:string)   id of the current project
        run_id(type: string)      id of the current run
        seq_id(type:string)       id of the sequence
        """
        return self.putative_rna_handler.get_putative_rna_path(user_id,
                                                               project_id,
                                                               run_id, 
                                                               p_rna_id)

    def get_putative_rna(self, user_id, rna_id, project_id):
        """ 
        Return(putative_rna)      the putative_rna defined by its id,
                                  None if no match
        user_id(type:string)      user id of the connected user
        rna_id(type:string)       the putative_rna id
        project_id(type:string)   project id the user is working on
        """
        return self.putative_rna_handler.get_putative_rna(user_id, rna_id,
                                                          project_id)


    def get_putative_rna_directory(self, user_id, project_id):
        """ 
        Return(putative_rna)      the putative_rna directory

        user_id(type:string)      user id of the connected user
        rna_id(type:string)       the putative_rna id
        project_id(type:string)   project id the user is working on
        """
        return self.putative_rna_handler.get_putative_rna_directory(user_id,
                                                                    project_id)
        

    def get_putative_rnas(self, user_id, project_id, run_id = None):
        """ 
        Return([putative_rna])    table of putative_rna for the specified
        user and project

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        """
        return self.putative_rna_handler.get_putative_rnas(user_id, project_id, run_id)

    def get_putative_rnas_by_runs(self, user_id, project_id):
        """ 
        Return([putative_rna])    table of putative_rna by run for the specified
        user and project

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        """
        return self.putative_rna_handler.get_putative_rnas_by_runs(user_id, project_id)

    def delete_putative_rnas(self, user_id, project_id, rnas_id):
        """ 
        Delete a table of putative_rna specified by a user_id, 
        a project_id and their id.

        user_id(type:string)      user id of the connected user
        rnas_id(type:[string])    table of rna's id to delete
        project_id(type:string)   project id the user is working on
        """
        self.putative_rna_handler.delete_putative_rnas(user_id,
                                                       project_id, 
                                                       rnas_id)
        
    def delete_run(self, user_id, project_id, run_id):
        """ 
        Delete all information on run_id and putative_rnas linked
        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        run_id(type:[string])     the run_id
        """
        prnas = self.putative_rna_handler.get_putative_rnas(user_id, project_id, run_id)
        aligns_id = []
        for prna in prnas:
            aligns_id.extend(prna.alignment)
        aligns_id = list(set(aligns_id)) 
        for align_id in aligns_id:
            self.align_handler.delete_alignment(user_id, project_id, align_id)
        self.putative_rna_handler.delete_run(user_id, project_id, run_id)

    def update_putative_rna(self, user_id, project_id, rna_id, rna):
        """
        Raise disk_error if no more space available
        
        Update the whole rna specified by its id
        user_id(type:string)         user id of the connected user
        project_id(type:string)      project id the user is working on
        rna_id(type:string)          the rna id to update
        rna(type:core.putative_rna)  the rna with the value to update
        """
        self.putative_rna_handler.update_putative_rna(user_id, project_id,
                                                      rna_id, rna)
        
    def update_putative_rnas_family(self, user_id, project_id, rnas_id, 
                                    new_family):
        """
        Raise disk_error if no more space available
        
        Update the family field of the putative_rnas specified
        
        user_id(type:string)      user id of the connected user
        rnas_id(type:[string])    table of rna's id to update
        new_family(type:string)   the new family
        project_id(type:string)   project id the user is working on
        """
        self.putative_rna_handler.update_putative_rnas_family(user_id,
                                                              project_id,
                                                              rnas_id,
                                                              new_family)
        
    def add_putative_rnas(self, user_id, project_id, prnas):
        """
        Raise disk_error if no more space available
        
        Add a table of putative_rnas to the project
        
        user_id(type:string)       user id of the connected user
        project_id(type:string)    project id the user is working on
        prna(type:[putative_rna])  the putative rnas objects to add
        """
        
        self.putative_rna_handler.add_putative_rnas(user_id, project_id, prnas)
        

    def combine_putative_rnas(self, user_id, project_id, prnas, combine_type = "basic_combine", **params):        
        """
        Raise disk_error if no more space available
        
        Combine all putative rnas given 
        user_id(type:string)      user id of the connected user
        project_id(type:string)   the project the user is working on
        prnas([putative_rnas])    the prnas to combine
        combine_type(string)      the combiner algorithm to use
        **params({string:string}) combiner parameters
        """  
        combiner = sequence_combiner()
        new_prnas = combiner.run(user_id, project_id, prnas, combine_type)
        prnas_id = []
        for prna in prnas:
            prnas_id.append(prna.sys_id)
        self.delete_putative_rnas(user_id, project_id, prnas_id)
        self.add_putative_rnas(user_id, project_id, new_prnas)


    ############################################################################
    ## SEQUENCE FUNCTIONS
    ##

    def get_sequence(self, user_id, sequence_id, project_id):
        """ 
        Return(sequence)          the sequence specified by its id for a 
        specified user and project
        
        user_id(type:string)      user id of the connected user
        sequence_id(type:string)  the squence id required
        project_id(type:string)   project id the user is working on
        """        
        return self.seq_handler.get_sequence(user_id, sequence_id, project_id)

    def get_sequences_id(self, user_id, project_id):
        """ 
        Return([string])          a table of all sequences id linked 
                                  to the project
        
        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        """ 
        return self.seq_handler.get_sequences_id(user_id, project_id)

    def get_sequence_directory(self, user_id, project_id):
        """
        Return(type:string)       the sequence directory

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        """
        return self.seq_handler.get_sequence_directory(user_id, project_id)

    def add_sequence(self, user_id, project_id, seq):
        """
        Raise disk_error if no more space available
        
        Add a sequence to the user

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        seq(type:sequence)        the sequence to add
        """
        self.seq_handler.add_sequence(user_id, project_id, seq)         
        
    def get_sequence_file(self, user_id, project_id, seq_id):
        """
        Return(type:string)       content of sequence file in fasta format

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        seq_id(type:string)       the id of the sequence
        """
        return self.seq_handler.get_sequence_file(user_id, project_id, seq_id)
    
    def get_sequence_file_path(self, user_id, project_id, seq_id):
        """
        Return(type:string)       sequence file path

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        seq_id(type:string)       the id of the sequence
        """        
        return self.seq_handler.get_sequence_file_path(user_id, project_id,
                                                       seq_id)
        
    def get_sequence_header(self, user_id, project_id,seq_id):
        """
        Return(type:string)       the sequence header

        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        seq_id(type:string)       the id of the sequence
        """
        return self.seq_handler.get_sequence_header(user_id, project_id, seq_id)

    def get_sequence_size_limitation(self):
        return common.get_nb_octet(self.config.get("storage", "sequence_size_limitation"))

    def get_nb_sequences_limitation(self):
        return int(self.config.get("storage", "nb_sequences_limitation"))

    ############################################################################
    ## USER FUNCTIONS
    ##

    def get_ids_from_authkey(self, id):
        """
        id(sting)      the id containing the user_id and the project_id
        return [user_id, project_id]
        """
        return self.user_handler.get_ids_from_authkey(id)

    def get_authkey(self, user_id, project_id):
        """
        user_id(sting)      the user_id
        project_id(string)  the project_id
        return the id
        """
        return self.user_handler.get_authkey(user_id, project_id)

    def user_has_data(self, user_id):
        """ 
        Return(type:boolean)      True if the user has data on disk, else False
        user_id(type:string)      user id of the connected user
        """
        return self.user_handler.has_data(user_id)

    def user_has_project(self, user_id, project_id):
        """ 
        Return(type:boolean)      True if the user has the specified project, False otherwise
        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        """
        return self.user_handler.has_project(user_id, project_id)
    
    def user_has_done_a_run(self, user_id, project_id):
        """ 
        Return(type:boolean)      True if the user has done a run on the specified project, False otherwise
        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        """
        return self.user_handler.user_has_done_a_run(user_id, project_id)
    
    def new_project(self, user_id):
        """
        Return(type:string)    project id
        
        user_id(string)        id of the connected user
        """
        return self.user_handler.new_project(user_id)
    
    def get_user_last_project_id(self, user_id):
        return self.user_handler.get_user_last_project_id(user_id)

    def update_user_last_project_id(self, user_id, project_id):
        self.user_handler.update_user_last_project_id(user_id, project_id)

    def get_last_run_id(self, user_id, project_id):
        return self.user_handler.get_last_run_id(user_id, project_id)

    def update_last_run_id(self, user_id, project_id, run_id):
        self.user_handler.update_last_run_id(user_id, project_id, run_id)

    def new_run(self, user_id, project_id):
        """
        Return(type:string)    run id
        
        user_id(string)        id of the connected user
        project_id(string)     id of the current project
        """
        return self.user_handler.new_run(user_id, project_id)

    def get_user_email(self, user_id, project_id):
        """
        Return(string)           the email address

        user_id(string)          the id of the connected user
        project_id(string)     id of the current project
        """
        return self.user_handler.get_user_email(user_id, project_id)

    def save_user_email(self, user_id, project_id, email):
        """
        Save the user email

        user_id(string)          the id of the connected user
        project_id(string)     id of the current project
        email(string)            the email address
        """
        self.user_handler.save_user_email(user_id, project_id, email)

    def get_user_directory(self, user_id):
        """
        Return(type:string)    user directory
        
        user_id(string)        id of the connected user
        """
        return self.user_handler.get_user_directory(user_id)

    def get_project_directory(self, user_id, project_id):
        """
        Return(string)         project directory

        user_id(string)        id of the connected user
        project_id(string)     id of the current project
        """
        return self.user_handler.get_project_directory(user_id, project_id)

    def get_user_used_space(self, user_id):
        info = self.user_handler.get_user_used_space(user_id)
        return info   

    def get_user_sequences_used_space(self, user_id, project_id):
        """
        user_id(string)            the id of the connected user
        project_id(string)       the project id
        """
        info = self.user_handler.get_project_sequences_used_space(user_id,
                                                                  project_id)
        return info   

    def get_available_space(self):
        return common.get_nb_octet(self.config.get("storage", "user_size_limitation"))

    def has_space_on_disk(self, user_id, project_id):
        max_user_size = common.get_nb_octet(self.config.get("storage", "user_size_limitation"))
       
        user_current_size = self.user_handler.get_user_used_space(user_id)

        if long(user_current_size) < long(max_user_size):
            max_project_size = common.get_nb_octet(self.config.get("storage", "project_size_limitation"))
            project_current_size = self.get_project_size(user_id, project_id)
            if long(project_current_size) < long(max_project_size):           
                return True
            else:
                return False
        else:
            return False

    def get_project_size(self, user_id, project_id):
        return self.user_handler.get_project_used_space(user_id, project_id)

    def get_sequences_disk_size(self, user_id, project_id):
        sum = 0
        ids = self.get_sequences_id(user_id, project_id)
        for id in ids:
            sum += self.get_sequence_disk_size(user_id, project_id, id)
        return sum

    def get_sequence_disk_size(self, user_id, project_id, seq_id):
         seq_path = self.get_sequence_file_path(user_id, project_id, seq_id)
         size = os.path.getsize(seq_path)
         return size

    def get_predictors_for_run(self, user_id, project_id, run_id):
        return self.user_handler.get_predictors_for_run(user_id, project_id, 
                                                        run_id)

    ############################################################################
    ## PREDICTOR FUNCTIONS
    ##

    def get_stdout_path(self, user_id, project_id, run_id, 
                        seq_id, softname, type):
        """
        Return(type:string)       the path of the stdout file

        user_id(type:string)      id of the connected user
        project_id(type:string)   id of the current project
        run_id(type: string)      id of the current run
        seq_id(type:string)       id of the sequence
        softname(type:string)     name of the predictor
        type(type:string)         predictor type
        """

        return self.predic_handler.get_stdout_path(user_id, project_id, 
                                                   run_id, seq_id, softname,
                                                   type)

    def get_stderr_path(self, user_id, project_id, run_id, 
                        seq_id, softname, type):
        """
        Return(type:string)       the path of the stderr file

        user_id(type:string)      id of the connected user
        project_id(type:string)   id of the current project
        run_id(type: string)      id of the current run
        seq_id(type:string)       id of the sequence
        softname(type:string)     name of the predictor
        type(type:string)         predictor type
        """

        return self.predic_handler.get_stderr_path(user_id, project_id, 
                                                   run_id, seq_id, softname,
                                                   type)


    ############################################################################
    ## ALIGNMENT FUNCTIONS
    ##

    def get_alignment_path(self, user_id, project_id, align_id):
        """
        Return(type:string)    alignment file path

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        align_id(string)       the id of the alignment
        """
        return self.align_handler.get_alignment_path(user_id, project_id,
                                                     align_id)

    def get_alignment_directory(self, user_id, project_id):
        """
        Return(type:string)    alignment directory

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        """
        return self.align_handler.get_alignment_directory(user_id, project_id)


    def add_alignments(self, user_id, project_id, alignments):
        """
        Raise disk_error if no more space available
        
        Add an alignment to the project
        
        user_id(type:string)      user id of the connected user
        project_id(type:string)   project id the user is working on
        align(type:alignement)    the alignment object to add
        """
        self.align_handler.add_alignments(user_id, project_id, alignments)

    def save_alignment_as_temporary(self, user_id, project_id, alignment):
        """ 
        Save the alignment but don't add it to the project
        
        user_id(type:string)       user id of the connected user
        project_id(type:string)    project id the user is working on
        alignment(type:alignement) the alignment object to add
        """

        return self.align_handler.save_alignment_as_temporary(user_id,
                                                              project_id,
                                                              alignment)

    def delete_alignment(self, user_id, project_id, align_id):
        """ 
        delete an alignment to the project
        
        user_id(type:string)       user id of the connected user
        project_id(type:string)    project id the user is working on
        align_id(type:alignement)  the alignment id to delete
        """
        align = self.get_alignment(user_id, project_id, align_id)
        if align is None:
            return
        for prna in align.rna_list:
            rna = self.get_putative_rna(user_id, prna.rna_id, project_id)
            if rna != None:
                aligns_to_delete = []
                for i in range(len(rna.alignment)):
                    if rna.alignment[i] == align_id:
                        aligns_to_delete.append(i)
                for i in aligns_to_delete:
                    del rna.alignment[i]
                    self.update_putative_rna(user_id, project_id, rna.sys_id, rna)
        self.align_handler.delete_alignment(user_id, project_id, align_id)
        
        
    def get_alignment(self, user_id, project_id, align_id):
        """
        Return(type:string)       the alignment
        user_id(string)           the id of the current user
        project_id(type:string)   project id the user is working on
        align_id(type:string)     the alignement id to return
        """
        return self.align_handler.get_alignment(user_id, project_id, align_id)

    def get_temporary_alignment(self, user_id, project_id, align_id):
        """
        Return(type:string)       the alignment
        user_id(string)           the id of the current user
        project_id(type:string)   project id the user is working on
        align_id(type:string)     the alignement id to return
        """
        return self.align_handler.get_temporary_alignment(user_id, project_id, align_id)

    def get_alignments(self, user_id, project_id):
        """
        Return(type:string)       the alignment
        user_id(string)           the id of the current user
        project_id(type:string)   project id the user is working on
        """
        return self.align_handler.get_alignments(user_id, project_id)

    def get_nb_alignments(self, user_id, project_id):
        """
        Return(type:int)          the number of alignments in the current project
        user_id(string)           the id of the current user
        project_id(type:string)   project id the user is working on
        """
        return self.align_handler.get_nb_alignments(user_id, project_id)
    
    ############################################################################
    ## GENOMES FUNCTIONS
    ##

    def get_species_names(self, domain):
        """
        Return([string])      the list of species names for a domain

        domain(string)        the domain from which we ask names
        """        
        return self.genome_handler.get_species_names(domain)

    def get_species_path(self, species):
        """
        Return(string)     the paths for a species and a domain
        
        species(string)    the species name
        """
        return self.genome_handler.get_species_path(species)

    def get_system_species_name(self, header):
        """
        Return(string)    the species system name for the specified path

        path(string)      the path of the databases
        """
        return self.genome_handler.get_system_species_name(header)

    def get_system_species_sequence_name(self, header):
        """
        Return(string)    the sequence system name

        seq_name(string)  the sequence name
        """
        return self.genome_handler.get_system_species_sequence_name(header)

    def get_species_ref_name(self, header):
        """
        Return((string, string))    return system species name and system 
                                    name for a sequence

        header(type:string)         the header of the sequence we want info
        """
        ref_name = self.get_system_species_name(header)
        ref_seq = self.get_system_species_sequence_name(header)
        return (ref_name, ref_seq)
    
    def get_header_species_name(self, header):
        return self.genome_handler.get_header_species_name(header)

    ############################################################################
    ## DATABASES FUNCTIONS
    ##
    def get_cluster_file(self, dbname):
        return self.db_handler.get_cluster_file(dbname)
    
    def get_db_names(self):
        """
        Return([string])    the list of available databases 
        """

        return self.db_handler.get_db_names()

    def get_db_path(self, db):
        """
        Return(string)    the path of the database named db, None if
                          if doesn't exist
        
        db(string)        the name of the db
        """        
        return self.db_handler.get_db_path(db)

    def get_system_db_name(self, path):
        """
        Return(string)    the database system name for the specified path

        path(string)      the path of the databases
        """
        return self.db_handler.get_system_db_name(path)

    def get_system_db_sequence_name(self, seq_name):
        """
        Return(string)    the sequence system name

        seq_name(string)  the sequence name
        """
        return self.db_handler.get_system_db_sequence_name(seq_name)

    def get_family_for_db(self, db, seq_name):
        """
        Return(string)    the family for a sequence

        db(string)        the name of the db from wich the sequence come from
        seq_name(string)  the sequence name
        """
        return self.db_handler.get_family_for_db(db, seq_name)

    ############################################################################
    ## EXPORT FUNCTIONS
    ##
    def create_export_file(self, user_id, project_id, rnas_to_export, format):
        """
        Return(string)                  the path to the export file
        
        user_id(string)                 the id of the current user
        project_id(string)              the id of the current project
        rnas_to_export([putative_rna])  table of putative_rna to export
        format(string)                  the export format
        """
        if format == "rnaml":
            path = tempfile.NamedTemporaryFile(suffix="export.xml").name
            export = rnaml()
        if format == "fasta":
            path = tempfile.NamedTemporaryFile(suffix="export.fna").name
            export = fasta_converter()
        if format == "gff":
            path = tempfile.NamedTemporaryFile(suffix="export.gff").name
            export = gff_converter()
        if format == "apollo_gff":
            path = tempfile.NamedTemporaryFile(suffix="export.gff").name
            export = apollo_gff_converter()

        export.write(rnas_to_export, path)
        return path



    ############################################################################
    ## TRACE FUNCTIONS
    ##
    def get_project_trace(self, user_id, project_id):
        """
        user_id(type:string)            user identifier
        project_id(type:string)         project identifier
        Returns(type:project_trace)     trace of the project
        """
        return self.trace_handler.get_project_trace(user_id, project_id)
        
    def update_project_trace(self, user_id, project_id, events):
        """
        events(type:[event])        list of events to add to the trace
        user_id(type:string)      user identifier
        project_id(type:string)   project identifier
        """
        self.trace_handler.update_project_trace(user_id, project_id, events)
        for e in events:
            if e.is_for_administrator == True:
                logging.getLogger("rnaspace").info(e.get_display())



    ############################################################################
    ## HELP FUNCTIONS
    ##
    def get_help_content(self):
        return self.config.get_help_content()

    ############################################################################
    ## OTHER FUNCTIONS
    ##
    def get_project_expiration_days(self):
        return self.config.get("storage", "project_expiration")
    
    def get_clustalw_exe(self):
        return self.config.get("software", "clustalw.exe")

    def get_rnafold_exe(self):
        return self.config.get("software", "rnafold.exe")

    def get_rnaplot_exe(self):
        return self.config.get("software", "rnaplot.exe")

    def get_rnaz_exe(self):
        return self.config.get("software", "rnaz.exe")

    def get_rnaalifold_exe(self):
        return self.config.get("software", "rnaalifold.exe")

    def get_unknown_user_name(self):
        return self.config.get("global", "unknown_user")
    
    def get_url_base(self):
        return self.config.get("global", "url_base")
