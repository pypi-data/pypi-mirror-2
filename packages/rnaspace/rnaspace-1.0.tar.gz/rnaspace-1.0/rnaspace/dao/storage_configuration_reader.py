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
from ConfigParser import ConfigParser
from ConfigParser import Error


CONF = {}
PREDICTORS_CONF_DIRECTORY = None


def update_conf(conf_path, predictors_conf_dir):
    global CONF
    global PREDICTORS_CONF_DIRECTORY

    PREDICTORS_CONF_DIRECTORY = predictors_conf_dir

    parser = ConfigParser()
    parser.read(conf_path)

    # browse sections
    for sec in parser.sections():
        # browse options of the current section
        for opt in parser.options(sec):
            value = parser.get(sec, opt)
            CONF.setdefault(sec, {})
            CONF[sec][opt] = value


class storage_configuration_reader(object):
    """ 
    Class configuration_reader: this object read the config file and return the 
    different configuration values
    """


    def get_storage_mode(self):
        """
        Return(type:string)     the storage mode to use. 

        Raise configuration_error object if the configuration file is invalide
        """
        try:
            return str(CONF['storage']['putative_rna_mode'])
        except KeyError:
            raise Error("Failed when parsing the rnaspace config file:" + 
                             "the option [putative_rna_mode] is missing in " + 
                             "the section [storage]")
        
    def get_storage_directory(self):
        """ 
        Return(type:string)     the path to the global storage directory
                                if exists, None otherwise. 

        Raise configuration_error object if the configuration file is invalide
        """
        try:
            directory = str(CONF['storage']['workspace_dir'])
            if os.path.isdir(directory):
                return directory
            else:
                return None
        except KeyError:
            raise Error("Failed when parsing the rnaspace config file:" + 
                             " the option [putative_rna_mode] is missing in " +
                             "the section [storage]")

    def get_predictors_conf_directory(self):
        """ 
        Return(type:string)     the path to the predirectors configuration
                                files directory if exists, None otherwise. 

        Raise configuration_error object if the configuration file is invalide
        """
        return PREDICTORS_CONF_DIRECTORY
        
    def get_user_directory(self, user_id):
        """
        Return(type:string)     the path to the user storage directory 
                                if exists, None otherwise. 

        user_id(type:string)    the user id
        """
        directory = self.get_storage_directory()
        if directory != None:
            user_directory = os.path.join(str(directory), str(user_id))
            if os.path.isdir(user_directory):
                return user_directory
            else:
                return None
        else: 
            return None

    def get_project_directory(self, user_id, project_id):
        """
        Return(type:string)      the path to the user's projet storage
                                 directory if exists, None otherwise. 

        user_id(type:string)     the user id
        project_id(type:string)  the project id
        """
        user_directory = self.get_user_directory(user_id)
        if user_directory != None:
            project_directory = os.path.join(str(user_directory),
                                             str(project_id))
            if os.path.isdir(project_directory):
                return project_directory
            else:
                return None
        else: 
            return None

    def get_putative_rna_directory(self, user_id, project_id):
        """
        Return(type:string)      the path to the putative rna directory 
                                 if exists, None otherwise. 

        user_id(type:string)     the user id
        project_id(type:string)  the project id
        """
        project_directory = self.get_project_directory(user_id, project_id)
        if project_directory != None:
            putative_rna_directory = os.path.join(str(project_directory),
                                                  "putative_rna")
            if os.path.isdir(putative_rna_directory):
                return putative_rna_directory
            else:
                return None
        else: 
            return None

    def get_putative_rna_serialization_file(self, user_id, project_id, run_id):
        """ 
        Return(type:string)      the path to the putative rna 
                                 serialization file.

        user_id(type:string)     the user id
        project_id(type:string)  the project id
        run_id(type:string)      the run id
        """
        putative_rna_directory = self.get_putative_rna_directory(user_id,
                                                                 project_id)
        putative_rna_directory = os.path.join(putative_rna_directory, run_id)
        if putative_rna_directory != None:
            serialization_file = os.path.join(str(putative_rna_directory),
                                              "putative_rna.dump")
            return serialization_file
        else: 
            return None

    def get_sequence_directory(self, user_id, project_id):
        """ 
        Return(type:string)      the path to the sequence directory 
                                 if exists, None otherwise. 

        user_id(type:string)     the user id
        project_id(type:string)  the project id
        """
        project_directory = self.get_project_directory(user_id, project_id)
        if project_directory != None:
            sequence_directory = os.path.join(str(project_directory),
                                              "sequence")
            if os.path.isdir(sequence_directory):
                return sequence_directory
            else:
                return None
        else: 
            return None

    def get_databases_directory(self):
        """
        Return(type:string)     the path to databases directory

        Raise configuration_error object if the configuration file is invalide
        """

        try:
            directory = str(CONF['storage']['db'])
            if os.path.isdir(directory):
                return directory
            else:
                return None
        except KeyError:
            raise Error("Failed when parsing the rnaspace config file:" +
                             "the option [db] is missing in the" + 
                             " section [storage]")

        
    def get_alignment_directory(self, user_id, project_id):
        """ 
        Return(type:string)      the path to the alignment directory 
        if exists, None otherwise. 

        user_id(type:string)     the user id
        project_id(type:string)  the project id
        """
        project_directory = self.get_project_directory(user_id, project_id)
        if project_directory != None:
            align_directory = os.path.join(str(project_directory),
                                           "alignment")      
            if os.path.isdir(align_directory):
                return align_directory
            else:
                return None
        else:
            return None


    def get_genomes_directory(self):
        """
        Return(type:string)     the path to genomes directory

        Raise configuration_error object if the configuration file is invalide
        """

        try:
            directory = str(CONF['storage']['genomes'])
            if os.path.isdir(directory):
                return directory
            else:
                return None
        except KeyError:
            raise Error("Failed when parsing the rnaspace config file:" +
                             "the option [genomes] is missing in the" + 
                             " section [storage]")


    def get_smtpserver(self):
        """
        Return(type:string)      the address of the smtp server
        """

        try:
            smtpserver = str(CONF['mailer']['smtpserver'])
            return smtpserver
        except KeyError:
            raise Error("Failed when parsing the rnaspace config file:" +
                             "the option [smtpserver] is missing in the" + 
                             " section [mailer]")

    def get_smtpserver_port(self):
        """
        Return(type:string)      the address of the smtp server
        """

        try:
            port = str(CONF['mailer']['port'])
            if port == '':
                return None
            return port
        except KeyError:
            return None


    def get_smtpserver_login(self):
        """
        Return(type:string)      the address of the smtp server
        """

        try:
            login = str(CONF['mailer']['login'])
            return login
        except KeyError:
            return None

    def get_smtpserver_password(self):
        """
        Return(type:string)      the address of the smtp server
        """

        try:
            password = str(CONF['mailer']['password'])
            return password
        except KeyError:
            return None


    def get_smtp_from_email(self):
        try:
            email = str(CONF['mailer']['from_email'])
            return email
        except KeyError:
            raise Error("Failed when parsing the rnaspace config file:" +
                             "the option [from_email] is missing in the" + 
                             " section [mailer]")


    def get_admin_email(self):
        try:
            email = str(CONF['mailer']['admin_email'])
            return email
        except KeyError:
            raise Error("Failed when parsing the rnaspace config file:" +
                             "the option [admin_email] is missing in the" + 
                             " section [mailer]")

    def get(self, section, identifier):
        try:
            value = str(CONF[section][identifier])
            return value
        except KeyError:
            raise Error("Failed when parsing the rnaspace config file: " +
                             "the identifier " + identifier +
                             " is missing in the section " + section)

    
