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
import os
import glob
import shutil

from rnaspace.core.conversion.gff_to_fasta import gff_to_fasta
from rnaspace.core.prediction.software_manager import software_manager
from rnaspace.core.prediction.threads_manager import threads_manager
from wrapper import wrapper

class comparative_analysis(wrapper):
    """
    This class implements the comparative analysis pipeline
    It first launches the selected conservation software.
    It then launches the aggregation tool and finally launches the
    inference software.

    """

    def __init__(self, opts, seq, user_id, project_id, run_id, p,
                 stderr, stdout, program_name, type, thread_name, version, exe):
        wrapper.__init__(self, opts, seq, user_id, project_id, run_id, p,
                         stderr, stdout, program_name, type, thread_name, 
                         version, exe)

        self.sm = software_manager()
        self.tm = threads_manager()
        self.conservation = self.opts['conservation_soft']
        self.aggregation = self.opts['aggregation_soft']
        self.inference = self.opts['inference_soft']
        self.species = p['species']


    def run(self):
        try:
            self.__run()
        except :
            import sys
            import traceback
            from rnaspace.core.trace.event import unknown_error_event
            (type, value, trace) = sys.exc_info()
            tb = "\n".join(traceback.format_exception(type, value, trace))
            error = "\n".join(traceback.format_exception_only(type, value))
            self.email_s.send_admin_tb(tb)
            ev = unknown_error_event(self.user_id, self.project_id, error,
                                     self.run_id, self.program_name)
            self.dm.update_project_trace(self.user_id, self.project_id, [ev])
            return


    def __run(self):

        t1 = time.clock()
        # get all species paths
        species_paths = []
        for s in self.species:
            # get all fasta file path for a species
            s_paths = self.dm.get_species_path(s)
            for s_path in s_paths:
                species_paths.append(s_path)

        sequence_path = self.dm.get_sequence_file_path(self.user_id, 
                                                       self.project_id, 
                                                       self.seq.id)

        ###################################################################
        ## lauch conservation software

        type = 'conservation'

        opts = self.opts['conservation_soft_opts']
        if opts is None:
            opts = self.sm.get_default_opts(self.conservation, type)

        blast_paths = []
        for species in species_paths:
            blast_path = self.get_temporary_file()
            blast_paths.append(blast_path)
            p = {'ref':species, 'blast_path':blast_path}            
            self.sm.launch_on_sequence(self.user_id, self.project_id, 
                                       self.run_id, self.conservation, type, 
                                       p, sequence_path, opts, self.tm)

        for t in self.tm.get_threads(self.user_id, self.project_id,
                                     self.run_id):
            t.join()
               

        ###################################################################
        ## lauch aggregation software

        type = 'aggregation'

        opts = self.opts['aggregation_soft_opts']

        if opts is None:
            opts = self.sm.get_default_opts(self.aggregation, type)

        gff_dir = self.get_temporary_directory()
        p = {'species_paths':species_paths, 'gff_dir':gff_dir, 
             'blast_paths':blast_paths}
        self.sm.launch_on_sequence(self.user_id, self.project_id, self.run_id,
                                   self.aggregation, type, p, sequence_path,
                                   opts, self.tm)

        for t in self.tm.get_threads(self.user_id, self.project_id,
                                     self.run_id):
            t.join()


        # convert gff files to fasta
        gff2fasta = gff_to_fasta()
        gffs = glob.glob(os.path.join(gff_dir, '*.gff'))
        for gff in gffs:
            (filepath, filename) = os.path.split(gff)
            (name, ext) = os.path.splitext(filename)
            fasta = os.path.join(filepath, name + '.fna')
            gff2fasta.convert(gff, fasta)
            

        ###################################################################
        ## lauch inference software

        type = 'inference'
        opts = self.opts['inference_soft_opts']

        if opts is None:
            opts = self.sm.get_default_opts(self.inference, type)

        fasta_files = glob.glob(os.path.join(gff_dir, '*.fna'))
        prog = self.conservation + '/' + self.aggregation + '/' + self.inference
        p = {'fasta_files':fasta_files, 'program_pipeline':prog}
        self.sm.launch_on_sequence(self.user_id, self.project_id, self.run_id,
                                   self.inference, type, p, sequence_path,
                                   opts, self.tm)

        for t in self.tm.get_threads(self.user_id, self.project_id,
                                     self.run_id):
            t.join()

        for path in blast_paths:
            os.remove(path)
        shutil.rmtree(gff_dir)
        t2 = time.clock()
        self.trace_predict_event(prog,0,0,t2 - t1,"comparative")
