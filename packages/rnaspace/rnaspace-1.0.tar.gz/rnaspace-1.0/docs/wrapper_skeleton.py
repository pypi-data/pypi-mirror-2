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

# we import the needed rnaspace modules
# you can look into these modules to see the objects used by RNAspace
from wrapper import wrapper
from rnaspace.core.putative_rna import putative_rna
from rnaspace.core.alignment import alignment
from rnaspace.core.secondary_structure import secondary_structure

# your class must inherit the wrapper class
class mypredictor(wrapper):

    def __init__(self, opts, seq, user_id, project_id, run_id, p,
                 stderr, stdout, program_name, type, thread_name, version, exe):
        # you first call the constructor of the wrapper module
        wrapper.__init__(self, opts, seq, user_id, project_id, run_id, p,
                         stderr, stdout, program_name, type, thread_name, 
                         version, exe)

    # your class must have the run method
    # it is the entry point of your predictor
    def run(self):

        # we first construct the options line using the 
        # self.opts dictionary
        options = ' '
        if self.opts is not None:
            for opt in self.opts:
                options += '-' + opt + ' ' + self.opts[opt]

        # we then get a temporary file to save the results
        result = self.get_temporary_file()
        # get the input sequence file path
        sequence_file = self.get_sequence_file_path()

        # we build the command line
        cmd = self.exe_path + options + ' ' + sequence_file + ' ' + result


        # and we execute it by calling the wrapper method "launch"
        self.launch(cmd)
        # finally, we write results in a way RNAspace can understand
        self.memorize_results(result)


    def memorize_results(self, result_file):

        prnas_list = []

        # we parse the result file
        for line in open(result_file):
    
            # DO THE JOB...

            # we get a new putative rna id
            # you need to use this method to obtain the id
            myid = self.id_gen.get_new_putativerna_id(self.user_id,
                                                      self.project_id,
                                                      self.seq.id)

            # we construct a secondary structure object
            structure = secondary_structure('bracket', 
                                            my_secondary_structure,
                                            self.program_name, 
                                            free_energy)

            # we create the putative rna object
            prna = putative_rna(myid, self.seq.id, 
                                long(begin_pos), 
                                long(end_pos), 
                                self.run_id,
                                user_id = myid,
                                sequence=thesequence, 
                                family=thefamily,
                                strand=thestrand,
                                domain=thedomain,
                                species=thespecies,
                                replicon=thereplicon,
                                structure=[structure],
                                score=the_score, 
                                program_name=self.program_name, 
                                program_version=self.program_version,
                                day=self.day, month=self.month,
                                year=self.year, alignment=[])

            # then we add the putative rna into a python list
            prnas_list.append(prna)

        # we add all the predicted rnas to RNAspace
        self.add_putative_rnas(self.user_id, self.project_id, prnas_list)
