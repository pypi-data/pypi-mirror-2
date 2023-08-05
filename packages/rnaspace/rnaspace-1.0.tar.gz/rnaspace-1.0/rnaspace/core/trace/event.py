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

# Define events to be traced
# Classes: event, event subclasses, hystory_rna



class event (object):
    """
    Description of an event to be traced in log file and if requested on stdout
    date(type:[integer])      event date [year month day hour minute second wday yday isdst]
    date_str(type:string)     date in string format
    type(type:string)         event type name
    """
    
    def __init__(self, user_id, project_id, mail_addresses):
        """
        Record common attributes
        """
        self.is_for_administrator = False
        self.date = time.localtime()
        
        year = str(time.localtime()[0])
        month = str(time.localtime()[1])
        if len(month) == 1:
            month = "0" + month
        day = str(time.localtime()[2])
        if len(day) == 1:
            day = "0" + day
        hour = str(time.localtime()[3])
        if len(hour) == 1:
            hour = "0" + hour        
        min = str(time.localtime()[4])
        if len(min) == 1:
            min = "0" + min
        sec = str(time.localtime()[5])
        if len(sec) == 1:
            sec = "0" + sec
        self.date_str = month +' '+ day +' '+ year +' '+ hour +' '+ min +' '+ sec

        self.user_id = user_id
        self.project_id = project_id
        self.run_id = None

        self.mail_addresses_str = ""
        for a in mail_addresses:
            if self.mail_addresses_str == "":
                self.mail_addresses_str = a
            else:
                self.mail_addresses_str = self.mail_addresses_str +" "+ a
                

    def get_display_base(self):
        line = self.date_str+"|"+ \
               self.user_id+"|"+ \
               self.project_id+"|"+ \
               self.mail_addresses_str
        return line


class history_rna(object):
    """ 
    Putative RNA description for trace (lighter than putative_rna class)
    rna_user_id(type:string)                        RNA user identifier
    seq_name(type:string)                           sequence identifier
    family(type:string)                             RNA family
    start(type:integer)                             RNA start position
    stop(type:integer)                              RNA stop position
    strand(type:string)                             RNA strand
    secondary_structures(type:[secondary_structure]) list of secondary_structure
    nb_alignment(type:integer)                      number of alignment
    """

    def __init__(self, rna_user_id, seq_name, family, start, 
                 stop, strand, secondary_structures, nb_alignment):
        self.rna_user_id = rna_user_id
        self.seq_name = seq_name        
        self.family = family  
        self.start = start  
        self.stop = stop  
        self.strand = strand  
        self.secondary_structures = secondary_structures  
        self.nb_alignment = nb_alignment

    

class add_seq_event (event):
    """ 
    An event that is adding (loading) a genomic sequence to a project
    seq_name(type:string)       name of the added sequence
    seq_size(type:integer)      size in nucleotide of the added sequence
    comment(type:string)        FASTA comment of the added sequence
    project_size(type:integer)  project size in Mb
    """
    
    def __init__(self, user_id, project_id, mail_addresses, seq_name, seq_size, comment, project_size):
        event.__init__(self, user_id, project_id, mail_addresses)
        self.is_for_administrator = True
        self.type = "ADD_SEQ"
        self.seq_name = seq_name
        self.seq_size = seq_size        
        self.comment = comment
        self.project_size = project_size

    def get_display(self):
        line = self.get_display_base()+"|"+ \
               self.type+"|"+ \
               self.seq_name+"|"+ \
               str(self.seq_size)+"|"+ \
               self.comment+"|"+ \
               str(self.project_size)
        return line


class predict_event (event):
    """ 
    An event that is predict putative RNAs on a genomic sequence with a wrapper of gene finder
    run_id(type:string)                 run identifier of run that launched the process
    seq_name(type:[string])             sequence name
    gene_finder_name(type:string)       gene finder name
    gene_finder_version(type:string)    gene finder version
    parameters(type:string)             gene finder parameters
    command(type:string)                gene finder executed command
    nb_prediction(type:integer)         number of predicted putative RNA
    nb_alignment(type:integer)          number of generated alignment
    running_time(type:string)           running time
    project_size(type:integer)          project size in Mb
    """ 
    
    def __init__(self, user_id, project_id, mail_addresses, run_id, seq_name, gene_finder_name, gene_finder_version, parameters,
                 command, nb_prediction, nb_alignment, running_time, project_size, aggregation_tag):
        event.__init__(self, user_id, project_id, mail_addresses)
        self.is_for_administrator = True
        self.type = "PREDICT"
        self.run_id = run_id
        self.seq_name = seq_name       
        self.gene_finder_name = gene_finder_name
        self.gene_finder_version = gene_finder_version        
        self.parameters = parameters
        self.command = command
        self.nb_prediction = nb_prediction  
        self.nb_alignment = nb_alignment 
        self.running_time = "%.2f" % running_time 
        self.project_size = project_size
        self.aggregation_tag = aggregation_tag

    def get_display(self):
        line = self.get_display_base()+"|"+ \
               self.type+"|"+ \
               self.run_id+"|"+ \
               self.seq_name+"|"+ \
               self.gene_finder_name+"|"+ \
               str(self.gene_finder_version)+"|"+ \
               str(self.nb_prediction)+"|"+ \
               str(self.nb_alignment)+"|"+ \
               self.command+"|"+ \
               str(self.running_time)+"|"+ \
               str(self.project_size)
        return line


class add_rna_event (event):
    """ 
    An event that is adding a putative RNA in a project
    rna(type:hystory_rna)       description of added RNA
    """
    
    def __init__(self, user_id, project_id, mail_addresses, rna_user_id, seq_name, 
                 family, start, stop, strand, secondary_structures, nb_alignment):
        event.__init__(self, user_id, project_id, mail_addresses)
        self.type = "ADD_RNA"
        self.rna = history_rna(rna_user_id, seq_name, family, start, 
                               stop, strand, secondary_structures, nb_alignment)

    def get_display(self):
        line = self.get_display_base()+"|"+ \
               self.type+"|"+ \
               self.rna.rna_user_id
        return line
        
        
class remove_rna_event (event):
    """ 
    An event that is removing putative RNAs in a project
    rna_user_ids(type:[string])       list of RNA user identifiers of putative RNAs to be deleted
    """
    
    def __init__(self, user_id, project_id, mail_addresses, rna_user_ids):
        event.__init__(self, user_id, project_id, mail_addresses)
        self.type = "REMOVE_RNA"
        self.rna_user_ids = rna_user_ids

    def get_display(self):
        l = ""
        for r in self.rna_user_ids:
            if l=="":
                l = r
            else:
                l = l +" "+ r
        line = self.get_display_base()+"|"+ \
               self.type+"|"+ \
               l
        return line


class edit_rna_event (event):
    """ 
    An event that is editing (modifying the description of) a putative RNA in a project
    Only modified attributes are specified with the new value.
    rna(type:hystory_rna)       description of edited RNA    
    """ 
    def __init__(self, user_id, project_id, mail_addresses, edited_rna_user_id, rna_user_id=None, seq_name=None, family=None, start=None, 
                 stop=None, strand=None, secondary_structures=None, nb_alignment=None):
        event.__init__(self, user_id, project_id, mail_addresses)
        self.type = "EDIT_RNA"
        self.edited_rna_user_id = edited_rna_user_id
        self.rna = history_rna(rna_user_id, seq_name, family, start, 
                               stop, strand, secondary_structures, nb_alignment)

    def get_display(self):
        if self.rna.rna_user_id == None:
            new_rna_user_id = self.edited_rna_user_id
        else:
            new_rna_user_id = self.rna.rna_user_id
        line = self.get_display_base()+"|"+ \
               self.type+"|"+ \
               self.edited_rna_user_id+"|"+ \
               new_rna_user_id
        return line


class add_alignment_event (event):
    """ 
    An event that is adding an alignment in a project
    rna_user_ids(type:[string])   list of RNA user identifier of putative RNA implicated in alignment
    """
    
    def __init__(self, user_id, project_id, mail_addresses, rna_user_ids):
        event.__init__(self, user_id, project_id, mail_addresses)
        self.type = "ADD_ALIGNMENT"
        self.rna_user_ids = rna_user_ids

    def get_display(self):
        l=""
        for r in self.rna_user_ids:
            if l == "":
                l = r
            else:
                l = l +" "+ r
        line = self.get_display_base()+"|"+ \
               self.type+"|"+ \
               l
        return line


class remove_alignment_event (event):
    """ 
    An event that is removing an alignment in a project
    rna_user_ids(type:[string])   list of RNA user identifier of putative RNA implicated in alignment
    """
    
    def __init__(self, user_id, project_id, mail_addresses, rna_user_ids):
        event.__init__(self, user_id, project_id, mail_addresses)
        self.type = "REMOVE_ALIGNMENT"
        self.rna_user_ids = rna_user_ids
    
    def get_display(self):
        l=""
        for r in self.rna_user_ids:
            if l=="":
                l = r
            else:
                l = l +" "+ r
        line = self.get_display_base()+"|"+ \
               self.type+"|"+ \
               l
        return line


class align_event (event):
    """ 
    An event that is alignment of putative RNAs by user
    rna_user_ids(type:[string])     list of RNA user identifier that are aligned
    software_name(type:string)      software name
    running_time(type:integer)      running time
    project_size(type:integer)      project size in Mb
    """
    
    def __init__(self, user_id, project_id, mail_addresses, rna_user_ids, software_name, running_time, project_size):
        event.__init__(self, user_id, project_id, mail_addresses)
        self.is_for_administrator = True
        self.type = "ALIGN"
        self.rna_user_ids = rna_user_ids
        self.software_name = software_name
        self.running_time = "%.2f" % running_time
        self.project_size = project_size

    def get_display(self):
        l=""
        for r in self.rna_user_ids:
            if l=="":
                l = r
            else:
                l = l +" "+ r
        line = self.get_display_base()+"|"+ \
               self.type+"|"+ \
               l+"|"+ \
               self.software_name+"|"+ \
               self.running_time+"|"+ \
               str(self.project_size)
        return line


class export_event (event):
    """ 
    An event that is exporting putative RNAs
    rna_user_ids(type:[string])   list of RNA user identifier of putative RNA to be exported
    format(type:string)           export format
    """
    
    def __init__(self, user_id, project_id, mail_addresses, rna_user_ids, format):
        event.__init__(self, user_id, project_id, mail_addresses)
        self.is_for_administrator = True
        self.type = "EXPORT_RNA"
        self.rna_user_ids = rna_user_ids
        self.format = format

    def get_display(self):
        l = ""
        for r in self.rna_user_ids:
            if l=="":
                l = r
            else:
                l = l +" "+ r
        line = self.get_display_base()+"|"+ \
               self.type+"|"+ \
               l+"|"+ \
               self.format
        return line


class error_event (event):
    """ 
    An event that is an error occurs
    message(type:string)            error description
    project_size(type:integer)      project size in Mb
    """
        
    def __init__(self, user_id, project_id, mail_addresses, message, project_size):
        event.__init__(self, user_id, project_id, mail_addresses)
        self.is_for_administrator = True
        self.type = "ERROR"
        self.message = message
        self.project_size = project_size

    def get_display(self):
        line = self.get_display_base()+"|"+ \
               self.type+"|"+ \
               self.message+"|"+ \
               str(self.project_size)
        return line 


class unknown_error_event(event):
    """
    Event indicating that an unknown error occured
    """
    def __init__(self, user_id, project_id, message, run_id=None,
                 predictor=None):
        event.__init__(self, user_id, project_id, "")
        self.is_for_administrator = True
        self.type = "UNKNOWN ERROR"
        self.message = message
        self.run_id = run_id
        self.predictor = predictor
        
    def get_display(self):
        fields = [self.get_display_base(), self.type, self.message]
        
        if self.run_id is not None:
            fields.append(self.run_id)
        if self.predictor is not None:
            fields.append(self.predictor)
            
        line = "|".join(str(field) for field in fields)
        return line


class prediction_error_event(event):
    """
    Event indicating that a prediction error occured
    """

    def __init__(self, user_id, project_id, mail_addresses, run_id, message,
                 predictor, cmd=None):
        """
        
        Arguments:
        - `user_id`: id of the user
        - `project_id`: id of the current project
        - `mail_addresses`: address of the user
        - `run_id`: id of the run that failed
        - `message`: error message
        - `cmd`: command used to launch external program
        - `predictor`: name of the predictor
        """
        
        event.__init__(self, user_id, project_id, mail_addresses)
        self.is_for_administrator = True
        self.run_id = run_id
        self.message = message
        self.type = "PREDICTION ERROR"
        self.cmd = cmd
        self.predictor = predictor

    def get_display(self):
        fields = [self.get_display_base(), self.type, self.run_id,
                  self.predictor, self.message]
        if self.cmd is not None:
            fields.append(self.cmd)
        line = "|".join(str(field) for field in fields)
        return line


class alignment_error_event(event):
    """
    Event indicating that a alignment error occured
    """


    def __init__(self, user_id, project_id, mail_addresses, message, aligner,
                 cmd=None):
        """
        
        Arguments:
        - `user_id`: id of the user
        - `project_id`: id of the current project
        - `mail_addresses`: address of the user
        - `message`: error message
        - `cmd`: command used to launch external program
        - `aligner`: name of the aligner
        """
        
        event.__init__(self, user_id, project_id, mail_addresses)
        self.is_for_administrator = True
        self.message = message
        self.type = "ALIGNMENT ERROR"
        self.cmd = cmd
        self.aligner = aligner
 
    def get_display(self):
        fields = [self.get_display_base(), self.type, self.aligner,
                  self.message]

        if self.cmd is not None:
            fields.append(self.cmd)
        line = "|".join(str(field) for field in fields)
        return line


class disk_error_event(event):
    """ 
    Event indicating that a disk error occured
    """
        
    def __init__(self, user_id, project_id, mail_addresses, message,
                 project_size, run_id=None):
        event.__init__(self, user_id, project_id, mail_addresses)
        self.is_for_administrator = True
        self.type = "DISK ERROR"
        self.message = message
        self.project_size = project_size
        self.run_id = run_id

    def get_display(self):
        fields = [self.get_display_base(), self.type, self.message,
                  str(self.project_size)]
        line = "|".join(str(field) for field in fields)
        return line

