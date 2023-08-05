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
import re
import logging

from exceptions import PredictorsConfError
from rnaspace.core.data_manager import data_manager
from rnaspace.core.trace.event import error_event

class predictor:
    """
    name           :  name of the software
    path           :  where is the module file
    exe_path       :  where is the exe file
    database       :  does the predictor need a database ?
    version        :  version number of the predictor
    type           :  known_{homology,rna_motif,specialized}, inference, 
                      conservation, abinitio
    simple_options :  list of options that do not take a parameter
    long_options   :  list of options that do take a paramter
    basic_options  :  list of basic_mode options
    default_simple :  default value of simple options (activated or not)
    options_default:  default value of long options
    options_params :  list of possible values for an option (if empty, we don't
                      care about the value of the option parameter)
    opts_param_flat:  same as options params but decoded
    options_desc   :  description of the option: will be displayed in the param
                      page
    options_view   :  specifiy how the user chooses an option: it can be a 
                      text area or a listbox
    help_text      :  help HTML code 

    """

    def __get_section(self, section, config):
        """
        Return({})         dictionary containing all options for a section
 
        section(string)    name of the section
        config({})         dictionary representing the conf file
        """
        try:
            sec = config[section]
        except KeyError:            
            raise PredictorsConfError(self.conf_file, section)
        return sec

    def __get_option(self, section, option, section_name):
        """
        Return({})             dictionary containing all options for a section
 
        section({})            section dictionary (get by __get_section)
        option(string)         the name of the option
        section_name(string)   the name of the section (just to print the error
                                                        the error message)
        """
        try:
            opt = section[option]
        except KeyError:
            raise PredictorsConfError(self.conf_file, section_name, option)
        return opt


    def __init__(self, conf_file, config={}, description = "", help = ""):
        """
        config        :  dictionnary that contains all the information
                         about the software
        description   :  little description of the software that is diplayed
                         when the mouse is over a '?'
        help          :  contains the HTML help page
        """
        
        self.logger = logging.getLogger("rnaspace")        

        self.data_m = data_manager()

        self.conf_file = conf_file
        self.options_view = {}
        self.default_simple = {}
        self.options_default = {}
        self.options_params = {}
        self.tools = {}

        general = self.__get_section('General', config)
        options = self.__get_section('Options', config)
        help = self.__get_section('Help', config)
        try:
            tools = self.__get_section('Tools', config)
        except PredictorsConfError:
            tools = None

        if tools is not None:
            for tool in tools:
                self.tools[tool] = self.__get_option(tools, tool, 'Tools')

        # get general information
        self.name = self.__get_option(general, 'name', 'General')
        self.path = self.__get_option(general, 'path', 'General')
        self.exe_path = self.__get_option(general, 'exe_path', 'General')
        self.speed = self.__get_option(general, 'speed', 'General')
        self.version = self.__get_option(general, 'version', 'General')
        self.type = self.__get_option(general, 'type', 'General')
        try:
            self.database = self.__get_option(general, 'database', 'General')
        except PredictorsConfError:
            self.database = '0'


        # get options
        self.simple_options = self.__get_option(options, 'simple',
                                                'Options').split(',')
        self.long_options = self.__get_option(options, 'long',
                                              'Options').split(',')
        self.basic_options = self.__get_option(options,'basic_options',
                                               'Options').split(',')
        params = {}
        view = {}
        desc = {}
        default = {}
        if self.long_options != ['']:
            params = self.__get_section('Options_Params', config)
            view = self.__get_section('Options_view', config)
        if self.simple_options != [''] or self.long_options != ['']:
            desc = self.__get_section('Options_desc', config)
            default = self.__get_section('Options_default_params', config)
       
        # get simple default values
        if self.simple_options != ['']:
            self.default_simple =\
                self.__get_option(default, 'default_simple',
                                  'Options_default_params').split(',')        

        # get long default values
        for key in default:
            if key != 'default_simple'and key != '':
                self.options_default[key] =\
                    self.__get_option(default, key, 'Options_default_params')
        
        # get options possible values
        for key in params:
            self.options_params[key] =\
                self.__get_option(params, key, 'Options_Params').split(',')
        self.opts_param_flat = {}
        self.decode_options_params()

        # get options descriptions
        self.options_desc = {}
        if self.long_options != ['']:
            for key in self.long_options:
                self.options_desc[key] = self.__get_option(desc, key,
                                                           'Options_desc')
        if self.simple_options != ['']:
            for key in self.simple_options:
                self.options_desc[key] = self.__get_option(desc, key,
                                                           'Options_desc')     
        # get options view type
        for key in self.long_options:
            if key != '':
                self.options_view[key] = self.__get_option(view, key,
                                                           'Options_view')

        # get help informations
        self.description = self.__get_option(general, "description", 
                                             "General")
        self.help_text = self.__get_option(help, "text", "Help")

    def decode_options_params(self):
        """
        transform '[1-5]' in '1,2,3,4,5'
        """
        pattern = '\[(.*)-(.*)\]'
        p = re.compile(pattern)
        for opt in self.options_params:            
            self.opts_param_flat.setdefault(opt, [])
            for val in self.options_params[opt]:
                result = p.match(val)
                if result is not None:
                    for i in range(int(result.group(1)),1+int(result.group(2))):
                        self.opts_param_flat[opt].append(str(i))
                elif val == '%':
                    for i in range(101):
                        self.opts_param_flat[opt].append(str(i))
                else:
                    self.opts_param_flat[opt].append(val)

    def get_opt_desc(self, opt):
        """
        Return(type:string)         the description of 'opt' option

        otp(string)                 the option
        """
        return self.options_desc[opt]

    def get(self, attr):
        """
        Return the attribute attr

        attr(string)                the attribute we want
        """
        try:
            attr = getattr(self, attr)
        except AttributeError:
            return None

        return attr

    def get_default_opts(self):
        opts = {}
        for opt in self.long_options:
            try:
                if self.options_default[opt] != "":
                    opts[opt] = self.options_default[opt]
            except KeyError:
                pass

        for opt in self.default_simple:
            if opt != "":
                opts[opt] = "True"

        return opts

    def get_predictor_class(self):
        """
        Return(Class)      the class of the predictor wrapper
        """

        # we try to find the module for this predictor
        # if we have an absolute path
        if self.path.find('/') != -1:
            # take the directory of the module
            path_list = self.path.split('/')
            path = '/'.join(i for i in path_list[:-1])
            # add it to sys.path
            if path not in sys.path:
                sys.path.append(path)
            name = path_list[-1].split('.')[0]
        else:
            # if we just have the name of the module,
            # we consider that the module is in the core.prediction.wrappers 
            # package
            current = os.path.dirname(os.path.abspath(__file__))
            current = os.path.join(current, 'wrappers')
            if os.path.abspath(current) not in sys.path:
                sys.path.append(os.path.abspath(current))
            name = self.path.split('.')[0]

        # try to import the predictor module
        try:        
            pred_mod = __import__(name)
        except ImportError:
            e = error_event("-","-","-","Module "+ name +".py not found.",0)
            self.logger.error(e.get_display())
            return None

        # try to get the predictor class
        try:
            pred_class = getattr(pred_mod, name)
        except AttributeError:
            e = error_event("-","-","-","Class " + name + " not found.",0)
            self.logger.error(e.get_display())
            return None

        return pred_class

    def check_parameters(self, params):
        error_msgs = {}
        param_flat = self.opts_param_flat
        for key in params:                
            # if the value is constrained
            if key in param_flat:               
                if param_flat[key] == ['<float>']:
                    if len(params[key]) > 0:
                        try:
                            float(params[key])
                        except:
                            error_msgs[key] = 'you need to specify a float'

                elif param_flat[key] == ['<int>']:
                    if len(params[key]) > 0:
                        try:
                            int(params[key])
                        except:
                            error_msgs[key] = 'you need to specify an integer'

                elif param_flat[key] == ['%']:
                    if ( params[key] != '' and 
                         (int(params[key]) > 100 or 
                          int(params[key]) < 0) ):
                        error_msgs[key] = 'option only take a percentage'
                elif (param_flat[key] != [''] and params[key] != '' and
                      params[key] not in param_flat[key]):
                    error_msgs[key] = 'option can not take "' +\
                        params[key] + '" value'
        return error_msgs


    def launch(self, user_id, project_id, run_id, opts, seq, params,
               stdout, stderr, type):
        """
        Return(threading.Thread)    return the thread that has been started
        
        user_id(string)             id of the connected user
        project_id(string)          id of the project the user is working on
        run_id(string)              id of the current thread
        opts({string:string})       options selected by the user
        seq(core.sequence)          the sequence given by the user
        params({string:string})     rnaspace intern parameters
        stdout(string)              path to stdout file for this thread
        stderr(string)              path to stderr file for this thread
        type(string)                alignment, inference, aggregation
        """
        
        p = params
        # give a name to the thread
        thread_name = user_id + project_id + run_id + self.name +\
            type + seq.id

        # get the predictor class
        pred_class = self.get_predictor_class()
        if pred_class is None:
            return None

        # instanciate predictor class
        if len(self.tools) > 0:
            pred = pred_class(opts, seq, user_id, project_id, run_id, p,
                              stderr, stdout, self.name, type, thread_name,
                              self.version, self.exe_path, self.tools)
        else:
            pred = pred_class(opts, seq, user_id, project_id, run_id, p,
                              stderr, stdout, self.name, type, thread_name,
                              self.version, self.exe_path)
        
        # run predictor
        pred.start()

        return pred
