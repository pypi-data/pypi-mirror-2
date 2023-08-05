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

from rnaspace.core.prediction.software_manager import software_manager
from rnaspace.core.data_manager import data_manager
from rnaspace.core.email_sender import email_sender
from rnaspace.core.trace.event import error_event

MAX_SPECIES = 4
# in octets
MAX_SEQUENCES_SIZE = 500 * 1024


class predict_model:

    def __init__(self):
        self.sm = software_manager()
        self.data_m = data_manager()
        self.email = email_sender()
        self.logger = logging.getLogger("rnaspace")

    def new_run(self, user_id, project_id):
        """
        Return(type:string)    the id of the new run
        
        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        """
        return self.data_m.new_run(user_id, project_id)

    def merge_opts(self, opts1, opts2):
        """        
        merge the two dictionnaries opts1 and opts2 in one

        Return({})       the merged dictionary

        opts1,opts2({})  two dictionaries
        """
        if opts1 is not None:
            if opts2 is not None:
                opts1.update(opts2)
            opts = opts1
        elif opts2 is not None:
            opts = opts2
        else:
            opts = None
        return opts

    def launch_software(self, user_id, project_id, run_id, params, level1,
                        level2):
        """
        launch selected software

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the id of the current run
        params({})             dictionary containing the form parameters
        level1({})             dictionary containing the options
                               available in predict page classify by type and
                               softname
        level2({})             dictionary containing the options
                               available in parameters view classify by type and
                               softname
        """

        # look for selected software in the form parameters
        for key in params:
            if (key.endswith('_known_name') or                 
                key.endswith('_abinitio_name')):
                # get softname and type
                softname = key.split('_')[0]
                type = key.split('_')[1]

                # get all options
                try:
                    opts1 = level1[type][softname]
                except:
                    opts1 = None      
                try:
                    opts2 = level2[type][softname]
                except:
                    opts2 = None      

                opts = self.merge_opts(opts1, opts2)

                # if it is a "known RNAs" software
                if key.endswith('_known_name'):               
                    p = {}
                    dbname = 'db_' + softname
                    # check if a databases is selected
                    if dbname in params.keys():
                        p['db'] = params[dbname] + '.fasta'
                    self.sm.add_job(user_id, project_id, run_id, 
                                    softname, 'known', opts, p)

                # if it is a abintio software
                elif key.endswith('_abinitio_name'):
                    p = {}                    
                    self.sm.add_job(user_id, project_id, run_id, 
                                    softname, 'abinitio', opts, p)

        try:
            # we try to get selected species: if no species selected, do nothing
            species = params['species_names']
            # if only one species selected, we create a list with this one.
            if not isinstance(species, list):
                species = [species]

            # get the selected software of the comparative analysis pipeline
            cons = params["cons_soft"]
            agg = params["agg_soft"]
            inf = params["inf_soft"]

            # get the options for each selected software
            type = "conservation"
            try:
                cons_opts = level2[type][cons]
            except:
                cons_opts = None      

            type = "aggregation"
            try:
                agg_opts = level2[type][agg]
            except:
                agg_opts = None      

            type = "inference"
            try:
                inf_opts = level2[type][inf]
            except:
                inf_opts = None      

            # and launch the comparative analysis predictor
            p = {}
            opts = {}
            p['species'] = species
            opts['conservation_soft'] = cons
            opts['aggregation_soft'] = agg
            opts['inference_soft'] = inf
            opts['conservation_soft_opts'] = cons_opts
            opts['aggregation_soft_opts'] = agg_opts
            opts['inference_soft_opts'] = inf_opts

            self.sm.add_job(user_id, project_id, run_id, 
                            'comparative', 'comparative', opts, p)
        except:
            pass

        combine = params.has_key('combine')
        self.sm.start_jobs(user_id, project_id, run_id, combine)

    def run_finished(self, user_id, project_id, run_id):
        """
        Return(type:boolean)   True if the execution of all selected
                               predictors has finished, False otherwise

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the id of the current run
        """
        return self.sm.run_finished(user_id, project_id, run_id)

    def run_failed(self, user_id, project_id, run_id):        
        """
        Return(type:[(predictor, message)])

        user_id(string)        the id of the current user
        project_id(string)     the id of the current project
        run_id(string)         the id of the current run
        """
        return self.sm.run_failed(user_id, project_id, run_id)

    def get_db_names(self, user_id, project_id):
        """
        Return(type:[])        a list containing the names of available database
        """
        dbnames = self.data_m.get_db_names()
        if dbnames is not None:
            dbnames = ['.'.join(name.split(".")[:-1]) for name in dbnames]
        else:
            message = "No databases found, " +\
                      "known predictors based on databases disable"
            self.trace_error_event(user_id, project_id, message)
        return dbnames

    def get_software_by_type(self, type):
        """
        Return(type:[])        a list of software name for a given type

        type(string):          type of the selected software
        """
        softs = self.sm.get_software_by_type(type)
        temp_softs = [ (soft.name.lower(), soft) for soft in softs]
        temp_softs.sort()
        return [soft for _, soft in temp_softs]

    def get_user_email(self, user_id, project_id):
        """
        Return(string)           the email address

        user_id(string)          the id of the connected user
        project_id(string)       the project id
        """
        return self.data_m.get_user_email(user_id, project_id)

    def get_species_names(self):
        """
        Return(type:[string]     the name of avilable species for the
                                 selected domain                                
        """
        domain = ["bacteria"]
        return self.data_m.get_species_names(domain)


    def has_user_done_a_run(self, user_id, project_id):
        """
        Return                True if the user has done a run yet,
                              False otherwise
        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        """
        try:
            return self.data_m.user_has_done_a_run(user_id, project_id)
        except:
            return False

    def get_nb_sequences(self, user_id, project_id):
        """
        Return                the number of uploaded sequence
        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        """
        try:
            seq_ids = self.data_m.get_sequences_id(user_id, project_id)
            return len(seq_ids)
        except:
            return 0

    def get_ids_from_authkey(self, id):
        """
        id(sting)      the id containing the user_id and the project_id
        return [user_id, project_id]
        """
        return self.data_m.get_ids_from_authkey(id)

    def get_authkey(self, user_id, project_id):
        """
        user_id(sting)      the user_id
        project_id(string)  the project_id
        return the id
        """
        return self.data_m.get_authkey(user_id, project_id)

    def is_an_authentification_platform(self):
        return self.data_m.is_an_authentification_platform()

    def trace_error_event(self, user_id, project_id, message):
        e = error_event(user_id, project_id,
                        self.data_m.get_user_email(user_id, project_id),
                        message,
                        self.data_m.get_project_size(user_id,project_id))
        self.logger.error(e.get_display())

    def comparative_activated(self, user_id, project_id):
        cons = self.get_software_by_type("conservation")
        agg = self.get_software_by_type("aggregation")
        inf = self.get_software_by_type("inference")
        species = self.get_species_names()

        if len(cons) == 0 or len(agg) == 0 or len(inf) == 0 or species is None:
            message = ""
            if len(cons) == 0:
                message += "No conservation soft found, "
            if len(inf) == 0:
                message += "No inference soft found, "
            if len(agg) == 0:
                message += "No aggregation soft found, "
            if species is None:
                message += "No genomes found, "
            message += "comparative analysis disable"
            self.trace_error_event(user_id, project_id, message)
            return False
        else:
            return True

    def known_activated(self, user_id, project_id):
        known = self.get_software_by_type("known")
        if len(known) == 0:
            message = "No known soft found, known RNAs part disable"
            self.trace_error_event(user_id, project_id, message)
            return False
        else:
            return True

    def abinitio_activated(self, user_id, project_id):
        abinitio = self.get_software_by_type("abinitio")
        if len(abinitio) == 0:
            message = "No abinitio soft found, abinitio part disable"
            self.trace_error_event(user_id, project_id, message)
            return False
        else:
            return True

    def get_mount_point(self):
        return self.data_m.get_mount_point()
