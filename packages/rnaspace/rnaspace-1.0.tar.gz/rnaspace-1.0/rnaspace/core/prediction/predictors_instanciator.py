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
import sys
import glob
import ConfigParser
import logging

from rnaspace.core.trace.event import error_event

import predictor

PATHS = os.environ["PATH"].split(":")

def readFile(file):
    """ read a file securely and return its data """

    try:
        fsock = open(file, "r")
        try:
            fdata = fsock.read()
        finally:
            fsock.close()
    except IOError:
        print "[!!] error reading file " + file
        return ""
        
    return fdata



class MyConfigParser(ConfigParser.ConfigParser):
    def optionxform(self, option):
        return str(option)


class predictors_instanciator:
    """
    This class control the configuration files reading and 
    the predictor instanciation.
    """

    def __init__(self):
        self.software = {}
        self.logger = logging.getLogger("rnaspace")

    def execution_test(self, soft):
        """
        Test if soft can be executed

        Return(boolean)     True if the predictor can be executed,
                            False otherwise
        """
        pred_class = soft.get_predictor_class()
        if pred_class is None:
            return False
        
        for path in PATHS:
            if os.path.isdir(path):
                exes = os.listdir(path)
                if soft.exe_path in exes:
                    return True

        if not os.path.isfile(soft.exe_path):
            e = error_event("-","-","-",soft.exe_path +" not found, "+soft.name+" disabled.",0)
            self.logger.error(e.get_display())
            return False

        return True

    def __load(self, file, config={}):
        """
        return a dictionnary: keys represent sections and each value is
        a dictionnary.

        configuration file format:
        ex:
        
        # a comment
        [section1]
        option1 = value1
        option2 = value2
        ...
        
        [section2]
        ...

        dictionary = {section1:{option1:value1,option2:value2},
                      section2:{option1:value1,option2:value2}, ...}
        """

        # create a ConfigParser and read the file
        conf = config.copy()
        cp = MyConfigParser()
        cp.read(file)
    
        # browse sections
        for sec in cp.sections():
            # browse options of the current section
            for opt in cp.options(sec):
                value = cp.get(sec, opt)
                conf.setdefault(sec, {})
                conf[sec][opt] = value[1:-1]

        return conf


    def load_soft_in_dir(self, path):
        """
        read all configuration files in 'path' and create an instance of
        'soft_type' software
        """
        conf_files = glob.glob(path + '/*.conf')
        for f in conf_files:
            (filepath, filename) = os.path.split(f)
            (shortname, ext) = os.path.splitext(filename)
            if (not shortname.endswith('_desc') and 
                not shortname.endswith('_help')):
                config = self.__load(f)
                try:
                    soft_type = config["General"]["type"]
                except:
                    print filename + ": type not found in General section"
                if soft_type.startswith("known"):
                    soft_type = "known"
                self.software.setdefault(soft_type, [])
                mod_name = 'rnaspace.core.prediction.predictor'
                mod = sys.modules[mod_name]
                soft_class = getattr(mod, 'predictor')
                soft = soft_class(f, config)
                if self.execution_test(soft):
                    self.software[soft_type].append(soft)


    def load_comparative(self):
        general = {'name':'comparative', 'path':'comparative_analysis', 
                   'exe_path':'', 'version':'', 'speed':'', 
                   'description': '', 'type':'comparative'}
        options = {'simple':'', 'long':'', 'basic_options':''}
        help = {'text':''}
        config = {'General':general, 'Options':options, 'Help':help}
        pred = predictor.predictor('comparative.conf', config)
        self.software['comparative'] = [pred]


    def load_available_soft(self, root, known_path="",
                            comp_path="", abinitio_path=""):
        """
        Return({string:[]})     dictionary: key => type of software
                                            value => list of predictor instances
        
        root(string)            root path of the configuration files
        """

        self.load_soft_in_dir(root)
        self.load_comparative()

        return self.software
