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

import thread
import re

from threads_manager import threads_manager
import predictors_instanciator as pi
from rnaspace.core.data_manager import data_manager
from rnaspace.core.email_sender import email_sender
from rnaspace.core.trace.event import disk_error_event
from rnaspace.core.exceptions import disk_error

class software_manager:

    software_dict = None
    threads = None
    jobs = {}

    def __init__(self):
        self.pred_inst = pi.predictors_instanciator()
        self.data_m = data_manager()
        predict_dir = self.data_m.get_predictors_conf_directory()
        if software_manager.software_dict is None:
            software_manager.software_dict = \
                self.pred_inst.load_available_soft(predict_dir)
            software_manager.threads = threads_manager()

        self.software = software_manager.software_dict
        self.threads = software_manager.threads
        self.email = email_sender()

    def add_job(self, user_id, project_id, run_id, softname, view_type, opts,
                params):
        """
        Add a job in a queue. The threads are not started. 'start_jobs' must
        be called to launch all the jobs for a run

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the id of the current run
        softname(string)       name of the software
        view_type(string)      'known', 'conservation', 'aggrgation',
                               'inference', 'abinitio'     
        opts({})               command line options
        params({})             wrapper parameters
        """
        self.jobs.setdefault(user_id, {})
        self.jobs[user_id].setdefault(project_id, {})
        self.jobs[user_id][project_id].setdefault(run_id, [])
        self.jobs[user_id][project_id][run_id].append((softname, view_type,
                                                       opts, params))

    def start_jobs(self, user_id, project_id, run_id, combine, 
                   tm_instance=None):
        """
        Start a thread that will starts all the jobs for a run.        

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the id of the current run
        combine(boolean)       True if the combine is required, False otherwise
        tm_instance(threads_manager) a threads_manager instance
        """
        thread.start_new_thread(self.launch, (user_id, project_id, run_id, 
                                              combine, tm_instance))

    def launch(self, user_id, project_id, run_id, combine, tm_instance=None):
        """
        Start all jobs added for a run in different threads

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the id of the current run
        combine(boolean)       True if the combine is required, False otherwise
        tm_instance(threads_manager) a threads_manager instance
        """

        email = self.data_m.get_user_email(user_id, project_id)

        url_base = self.data_m.get_url_base()
        if url_base[-1] == '/':
            url_base = url_base[:-1]
        mount_point = self.data_m.get_mount_point()
        if mount_point[0] == '/':
            if len(mount_point) > 1:
                mount_point = mount_point[1:]
            else:
                mount_point = ""
        full_url = url_base + "/" + mount_point

        run_jobs = self.jobs[user_id][project_id][run_id]

        # get all sequences for the current run
        seq_ids = self.data_m.get_sequences_id(user_id, project_id)
        sequences = []
        for seq_id in seq_ids:
            sequences.append(self.data_m.get_sequence_file_path(user_id, 
                                                                project_id, 
                                                                seq_id))
        for (softname, view_type, opts, params) in run_jobs:
            soft = self.get_software(softname, view_type)
            # default options if no options specified
            if opts is None:
                opts = soft.get_default_opts()
            # launch predictor on each sequence
            for seq in sequences:
                self.launch_on_sequence(user_id, project_id, run_id, softname,
                                        view_type, params, seq, opts, 
                                        tm_instance)

        # wait for all threads to finish
        if tm_instance is None:
            ts = self.threads.get_threads(user_id, project_id, run_id) 
        else:
            ts = tm_instance.get_threads(user_id, project_id, run_id)    

        for t in ts:
            t.join()

        # alert the user if the run failed
        failed_soft = self.run_failed(user_id, project_id, run_id)
        if len(failed_soft) != 0:
            if email is not None and len(email) > 0:
                self.email.send_user_failed_email(user_id, project_id, 
                                                  run_id, failed_soft, 
                                                  email, full_url)
            return

        # make the combine if requested
        if combine:
            err = self.combine(user_id, project_id, run_id)
            if err:
                if email is not None and len(email) > 0:                
                    self.email.send_user_failed_email(user_id, project_id,
                                                      run_id, [err], email,
                                                      full_url)
                return

        # everything is ok.
        # send a mail if address provided
        if email is not None and len(email) > 0:
            self.email.send_user_email(user_id, project_id, run_id, 
                                       email, full_url)

    def launch_on_sequence(self, user_id, project_id, run_id, softname, 
                           view_type, params, seq, opts, tm_instance=None):

        soft = self.get_software(softname, view_type)
        seq_id = seq.split('/')[-1].split('.')
        seq_id = '.'.join(s for s in seq_id[0:-1])
        sdata = self.data_m.get_sequence(user_id, seq_id, project_id)
        stderr = self.data_m.get_stderr_path(user_id, project_id, run_id,
                                             seq_id, softname, view_type)
        stdout = self.data_m.get_stdout_path(user_id, project_id, run_id,
                                             seq_id, softname, view_type)
        t = soft.launch(user_id, project_id, run_id, opts, sdata, params, 
                        stdout, stderr, view_type)
            
        if t is not None:
            if tm_instance is None:
                self.threads.add_thread(user_id, project_id, run_id, t)
            else:
                tm_instance.add_thread(user_id, project_id, run_id, t)

    def combine(self, user_id, project_id, run_id):
        """
        Combine predictions of the current run
        
        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the run id
        """
        prnas = self.data_m.get_putative_rnas(user_id, project_id, run_id)
        try:
            self.data_m.combine_putative_rnas(user_id, project_id, prnas)
            return None
        except disk_error, e:
            email = self.data_m.get_user_email(user_id, project_id)
            ev = disk_error_event(user_id, project_id, email, e.__str__(), "combine", run_id)   
            self.data_m.update_project_trace(user_id, project_id, [ev])
            return ("combine", e.__str__())

    def run_failed(self, user_id, project_id, run_id):        
        """
        Return(type:[(predictor, message)])

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the id of the current run
        """
        messages = []
        trace = self.data_m.get_project_trace(user_id, project_id)

        # check if an error occured during the wrappers's "run" method
        # the execution of an external program, the record of a rna or analignment
        errors = trace.get_errors_events(run_id) 
        for error in errors:
            messages.append((error.predictor, error.message))
        
        return messages

    def run_finished(self, user_id, project_id, run_id):
        """
        Return(type:boolean)   True if the execution of all selected
                               predictors has finished, False otherwise

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the id of the current run
        """
        return self.threads.run_threads_finished(user_id, project_id, run_id)

    def check_parameters(self, softname, type, params):
        """
        Check if the value enter by the user are correct

        Return({})      list of error messages classified by option

        params({})      list of options and their selected values 
        """
        soft = self.get_software(softname, type)
        return soft.check_parameters(params)


    def get_software(self, softname, type):
        """
        Return(type:predictor) object representing the software named 'softname'

        softname(string):      name of the selected software
        type(string):          type of the selected software
        """
        for soft in self.software[type]:
            if soft.name == softname:
                return soft

    def get_specialized_softs(self):
        """
        Return([soft])        list of known_specialized soft
        """
        softs = []
        for soft in self.software["known"]:
            if soft.type == "known_specialized":
                softs.append(soft.get('name'))
        return softs

    def get_software_by_type(self, type):
        """
        Return(type:[string])  list of software for a given type

        type(string):          type of the selected software
        """
        softs = []
        if type not in self.software:
            return softs
        for soft in self.software[type]:
            softs.append(soft)
        return softs
                                  
    def get_default_opts(self, softname, softtype):
        soft = self.get_software(softname, softtype)
        return soft.get_default_opts()

    def get_software_help(self, type):
        """
        Return({softname:help})  help pages for all predictors of type "type"

        type(string)             the type of predictors we want the help
        """

        help = {}
        t = type
        if type.startswith("known"):
            t = "known"
            
        softs = self.get_software_by_type(t)
        for soft in softs:
            if soft.type == type:
                help[soft.name] = soft.help_text

        return help
            
    def get_parameters_help(self, softname, type):
        """
        Return(type:string)     help page of the soft

        softname(string):       name of the selected software
        type(string):           type of the selected software
        """
        soft = self.get_software(softname, type)
        return soft.get('parameters')

    def get_software_desc(self, type):
        """
        Return({softname:help})  help pages for all predictors of type "type"

        type(string)             the type of predictors we want the help
        """
        desc = {}

        softs = self.get_software_by_type(type)
        for soft in softs:            
            desc[soft.name] = soft.description

        return desc
  
    def get_options_params(self, softname, type):
        soft = self.get_software(softname, type)
        return soft.get('options_params')

    def get_software_type(self, softname):
        """
        Return(type:string)  the software type
        softname(string):    the software name
        """
        for type in self.software:
            for soft in self.software[type]:
                if re.search(soft.name, softname):
                    return soft.type
        return ""
