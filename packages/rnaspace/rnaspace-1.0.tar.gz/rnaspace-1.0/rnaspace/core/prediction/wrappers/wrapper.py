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

import sys
import os
import threading
import subprocess
import time
import tempfile

from rnaspace.core.exceptions import disk_error
from rnaspace.core.conversion.rnaml import rnaml
from rnaspace.core.data_manager import data_manager
from rnaspace.core.id_tools import id_tools
from rnaspace.core.trace.event import predict_event, prediction_error_event, disk_error_event
from rnaspace.core.email_sender import email_sender

class wrapper(threading.Thread):

    def __init__(self, opts, seq, user_id, project_id, run_id, p, stderr,
                 stdout, program_name, type, thread_name, version, exe,
                 tools=None):

        threading.Thread.__init__(self, name=thread_name)

        self.dm = data_manager()
        self.stock = rnaml()
        self.id_gen = id_tools()
        self.email_s = email_sender()
        self.tools = tools

        # options list
        self.opts = opts
        # the input sequence object
        self.seq = seq
        # the user_id        
        self.user_id = user_id
        # the project_id
        self.project_id = project_id
        # the run_id
        self.run_id = run_id
        # stderr and stdout
        self.stderr = stderr
        self.stdout = stdout

        if p.has_key('blast_path'):
            self.blast_path = p['blast_path']
        if p.has_key('db'):
            database = p['db']
            self.db = self.dm.get_db_path(database)            
        if p.has_key('ref'):
            database = p['ref']
            self.db = database
        if p.has_key('species_paths'):
            self.species_paths = p['species_paths']
        if p.has_key('gff_dir'):
            self.gff_dir = p['gff_dir']
        if p.has_key('blast_paths'):
            self.blast_paths = p['blast_paths']
        if p.has_key('fasta_files'):
            self.fasta_files = p['fasta_files']
        if p.has_key('program_pipeline'):
            self.program_pipeline = p['program_pipeline']
        self.prnas_to_add = []
        self.aligns_to_add = []

        # date of the instanciation
        self.year = str(time.localtime()[0])
        self.month = str(time.localtime()[1])
        self.day = str(time.localtime()[2])
        self.hour = str(time.localtime()[3])
        self.min = str(time.localtime()[4])
        self.sec = str(time.localtime()[5])

        self.program_name = program_name

        if p.has_key('db'):
            try:
                (dbdir, dbname) = os.path.split(self.db)
                (shortname, ext) = os.path.splitext(dbname)
                self.program_name += '/' + shortname
            except AttributeError:
                pass
                
        self.program_version = version
        self.exe_path = exe
        self.type = type

        self.grid_engine = self.dm.config.get("execution","grid_engine")
        self.grid_engine_cmd = self.dm.config.get("execution","grid_engine.cmd")
        self.grid_engine_outfile_arg = self.dm.config.get("execution","grid_engine.outfile_arg") 
        self.grid_engine_errorfile_arg = self.dm.config.get("execution","grid_engine.errorfile_arg")

        self.tmp_dir = self.dm.config.get("storage","tmp_dir")

    def get_temporary_directory(self, suffix=None, prefix=None):
        """
        Return a temporary directory
        """
        if suffix is not None:
            if prefix is not None:
                tmp_dir = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=self.tmp_dir)
            else:
                tmp_dir = tempfile.mkdtemp(suffix=suffix, dir=self.tmp_dir)
        else:
            if prefix is not None:
                tmp_dir = tempfile.mkdtemp(prefix=prefix, dir=self.tmp_dir)
            else:
                tmp_dir = tempfile.mkdtemp(dir=self.tmp_dir)
        return os.path.join(tmp_dir)

    def get_temporary_file(self, suffix=None, prefix=None):
        """
        Return a temporary file
        """
        if suffix is not None:
            if prefix is not None:
                return tempfile.NamedTemporaryFile(suffix=suffix,
                                                   prefix=prefix,
                                                   dir=self.tmp_dir).name
                                                   
            else:
                return tempfile.NamedTemporaryFile(suffix=suffix,
                                                   dir=self.tmp_dir).name
        else:
            if prefix is not None:
                return tempfile.NamedTemporaryFile(prefix=prefix,
                                                   dir=self.tmp_dir).name
                                                   
            else:
                return tempfile.NamedTemporaryFile(dir=self.tmp_dir).name


    def run(self):
        print "You must write a 'run' method in your wrapper !"


    def launch(self, cmd):

        if (self.grid_engine=="true"):
            # put cmd in a shell file and call the grid engine batch job submiter
            tmp_cmd_file = self.get_temporary_file()
            tmp_out_file = tmp_cmd_file+".out"
            tmp_error_file = tmp_cmd_file+".error"            
            ftmp = open(tmp_cmd_file, 'w')
            ftmp.write(cmd)
            ftmp.close()
            CMD = self.grid_engine_cmd +" "+ self.grid_engine_outfile_arg +" "+ tmp_out_file+" " \
                  + self.grid_engine_errorfile_arg +" "+ tmp_error_file +" "+ tmp_cmd_file
        else:
            CMD = cmd

        envir = os.environ

        try:
            stderr = open(self.stderr,'w')
            stdout = open(self.stdout,'w')
            retcode = subprocess.call(CMD, shell=True, stderr=stderr, 
                                      stdout=stdout, env=envir)
            stderr.close()
            stdout.close()

        except :
            mess = self.create_failed_message("Error launching subprocess in wrapper:launch.")
            self.trace_error_event(self.user_id, self.project_id, mess, cmd)
            sys.exit(1)  # stop thread
 
        if (self.grid_engine=="true"):   
            os.remove(tmp_cmd_file)
            os.remove(tmp_out_file)
            os.remove(tmp_error_file)               

        self.if_exec_error(retcode, CMD)


    def if_exec_error(self, retcode, cmd):
        if retcode != 0:
            mess = self.create_failed_message()
            self.trace_error_event(self.user_id, self.project_id, mess, cmd)
    

    def create_failed_message(self, message=None):
        if message is None:
            stderr = open(self.stderr,'r')
            mess = stderr.read()
            stderr.close()
            mess = mess.replace('\n', ' ')
        else:
            mess = message
        return mess


    def trace_error_event(self, user_id, project_id, mess, cmd):
        self.email_s.send_admin_failed_email(self.user_id, self.project_id,
                                             self.run_id, self.program_name,
                                             cmd)

        message = "Error running %s %s"%(self.program_name, mess)
        message = message + ". See run " + self.run_id + " description."
        mail = self.dm.get_user_email(user_id, project_id)
        e = prediction_error_event(user_id, project_id, mail, self.run_id,
                                   message, self.program_name, cmd)
        self.dm.update_project_trace(self.user_id, self.project_id, [e])


    def trace_predict_event(self, cmd, nb_prediction, nb_alignment,
                            running_time, aggregation_tag):
        e = predict_event(self.user_id, self.project_id,
                          self.dm.get_user_email(self.user_id,self.project_id),
                          self.run_id, self.seq.id,
                          self.program_name, self.program_version,
                          self.opts,
                          cmd, nb_prediction, nb_alignment, running_time,
                          self.dm.get_project_size(self.user_id,self.project_id),
                          aggregation_tag)
        self.dm.update_project_trace(self.user_id,self.project_id, [e])



    #########################################################################
    ## HELPER FUNCTIONS
    ##

    def get_family(self, header):
        if header.startswith('>'):
            return header.split('|')[0][1:]
        else:
            return header.split('|')[0]

    def get_sequence_file_path(self):        
        return self.dm.get_sequence_file_path(self.user_id, self.project_id,
                                              self.seq.id)

    def get_sequence_header(self):
        return self.dm.get_sequence_header(self.user_id, self.project_id,
                                           self.seq.id)

    def get_species_names(self, header):
        return self.dm.get_species_ref_name(header)


    def add_alignments(self, alignments):
        if len(alignments) == 0:
            return
        try:
            self.dm.add_alignments(self.user_id, self.project_id, alignments)
        except disk_error, e:
            mail = self.dm.get_user_email(self.user_id,self.project_id)
            ev = disk_error_event(self.user_id, self.project_id, mail, e.__str__() + str(self.program_name), self.run_id)
            
            self.dm.update_project_trace(self.user_id, self.project_id, [ev])


    def add_putative_rnas(self, prnas):
        if len(prnas) == 0:
            return
        try:
            self.dm.add_putative_rnas(self.user_id, self.project_id, prnas)  
        except disk_error, e:
            mail = self.dm.get_user_email(self.user_id,self.project_id)
            ev = disk_error_event(self.user_id, self.project_id, mail, e.__str__() + str(self.program_name), self.run_id)
            
            self.dm.update_project_trace(self.user_id, self.project_id, [ev])

    def get_header_species_name(self, header):
        return self.dm.get_header_species_name(header)
