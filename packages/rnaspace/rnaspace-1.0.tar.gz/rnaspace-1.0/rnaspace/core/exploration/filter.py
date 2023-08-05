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


import re

class selection_criteria(object):
    """ Class selection_criteria: gathers information on a selection criteria
    """
    # store all the available combinaison between a criteria and its operators
    available_combinaisons = {"user_id": ["=", "!="],
                              "family":[ "=", "!="],
                              "genomic_sequence_id":[ "=", "!="],
                              "organism":["=", "!="], 
                              "strain": ["=", "!="], 
                              "domain": ["=", "!="], 
                              "species": ["=", "!="], 
                              "program_name": ["=", "!="], 
                              "score": ["=", "!=", "<", "<=", ">", ">="],
                              "replicon": ["=", "!="], 
                              "start_position": ["=", "!=", "<", "<=", ">", ">="], 
                              "stop_position": ["=", "!=", "<", "<=", ">", ">="], 
                              "strand": ["=", "!="], 
                              "size": ["=", "!=", "<", "<=", ">", ">="], 
                              "alignment": ["=", "!=", "<", "<=", ">", ">="], 
                              "run": ["=", "!="]
                              }
    
    def __init__(self, characteristic, op='', v=None):
        """ Build a selection_criteria object defined by
            characteristic(type:string)  characteristic name                
            operator(type:string)        operator value (has to match an 
                                         operator available for the given
                                         characteristic)                    
            value(type:string)           the selection criteria value     
        """
        if self.__is_a_characteristic(characteristic):
            self.characteristic = characteristic
            if op=='':
                self.operator = selection_criteria.available_combinaisons[characteristic][0]
            else:
                self.operator = op
            self.value = v
        else:
            raise TypeError, (characteristic + " is not an available characteristic value " + selection_criteria.available_combinaisons.keys())

    def __is_a_characteristic(self, characteristic):
        """ Return(type:boolean) True if the given characteristic is correct, else False
        """
        return selection_criteria.available_combinaisons.has_key(characteristic)
        
class filter (object):
    """ Class filter: defines characteristics to build a putative_rnas filter
    """

    def __init__(self, id = "filter"):
        """ Build a filter object defined by
            id(type:string)               filter id                         
            name(type:string)             filter name                           
            all_criteria(type:[])         table of all the selection criteria of
                                          the filter                                
        """
        self.id = id
        self.name = "none"
        self.all_criteria = []

    def __len__(self):
        """ Return(type:integer) the filter length
        """
        return len(self.all_criteria)
    
    def add_criteria(self, criteria):
        """ add a criteria to the filter
            criteria(type:selection_criteria)    the criteria to add
        """
        self.all_criteria.append(criteria)

    def delete_all(self):
        """ delete all the filter's criteria 
        """
        self.all_criteria = []

    def get_criteria(self, id_criteria):
        """ Return(type:selection_criteria) the criteria specified by its position 
            into the table
            id_criteria(type:integer)      index of the criteria into the table   
        """ 
        return self.all_criteria[id_criteria]

    def run(self, arns):
        """ Return(type:[putative_rna])  a table of putative_rna filtered
            arns(type:[putative_rna])    table of putative_rna to filter
        """
        filtered_arns = []
        if (len(self) > 0):
            for i in range(len(arns)): # for each arns
                this_arn_is_ok = 1 # by default it is
                for j in range(len(self)): # for each criteria of filtration
                    characteristic_value = arns[i].get_x(self.get_criteria(j).characteristic)
                    if type(characteristic_value) == type([]):
                        characteristic_value = len(characteristic_value)
                    if (self.get_criteria(j).operator == "="):
                        rna_value = str(characteristic_value)
                        value_to_match = str(self.get_criteria(j).value)
                        value_to_match = value_to_match.replace("*", ".*")
                        value_to_match = value_to_match.replace("?", ".")
                        value_to_match = value_to_match.replace("_", ".")
                        value_to_match = "^" + value_to_match + "$"
                        try:
                            if not re.search(value_to_match, rna_value, re.IGNORECASE):      
                                this_arn_is_ok = 0 # this arn doesn't fit this criteria
                        except:
                            pass
                    elif (self.get_criteria(j).operator == "!="):
                        rna_value = str(characteristic_value)
                        value_to_match = str(self.get_criteria(j).value)
                        value_to_match = value_to_match.replace("*", ".*")
                        value_to_match = value_to_match.replace("?", ".")
                        value_to_match = value_to_match.replace("_", ".")
                        value_to_match = "^" + value_to_match + "$"
                        try: 
                            if re.search(value_to_match, rna_value, re.IGNORECASE):      
                                this_arn_is_ok = 0 # this arn doesn't fit this criteria
                        except:
                            pass    
                    elif (self.get_criteria(j).operator == "<"):
                        if (not(float(characteristic_value) < float(self.get_criteria(j).value))):
                            this_arn_is_ok = 0 # this arn doesn't fit this criteria 
                    elif (self.get_criteria(j).operator == "<="):
                        if (not(float(characteristic_value) <= float(self.get_criteria(j).value))):
                            this_arn_is_ok = 0 # this arn doesn't fit this criteria 
                    elif (self.get_criteria(j).operator == ">"):
                        if (not(float(characteristic_value) > float(self.get_criteria(j).value))):
                            this_arn_is_ok = 0 # this arn doesn't fit this criteria 
                    elif (self.get_criteria(j).operator == ">="):
                        if (not(float(characteristic_value) >= float(self.get_criteria(j).value))):
                            this_arn_is_ok = 0 # this arn doesn't fit this criteria
                if (this_arn_is_ok == 1): # if this arn went throught all the criteria, then add it to the result table
                    filtered_arns.append(arns[i])   
        else: # If no filter, just send back the arns table
            filtered_arns = arns
        
        return filtered_arns # return the final result
