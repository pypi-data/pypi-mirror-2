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
import operator
import tempfile

from rnaspace.core.data_manager import data_manager
from rnaspace.core.conversion.cgview_converter import cgview_converter
from rnaspace.core.trace.event import export_event, remove_rna_event
from rnaspace.core.exploration.filter import filter
from rnaspace.core.exploration.filter import selection_criteria

class explore_model(object):
    """ Class explore_model: the model of the explore web page
    """  
    
    max_item_length = 20
    show_allowed = [20, 50, 100, 500, 1000]
    terse_set = [["ID", "user_id"], ["Seq name", "genomic_sequence_id"], ["Family", "family"], ["Start", "start_position"], ["End", "stop_position"], ["Size", "size"], ["Strand", "strand"], ["Species", "species"], ["Domain", "domain"], ["Replicon", "replicon"], ["Software", "program_name"], ["Align.", "alignment"], ["Run", "run"]]
    all = [["ID", "user_id"], ["Seq name", "genomic_sequence_id"], ["Family", "family"], ["Start", "start_position"], ["End", "stop_position"], ["Size", "size"], ["Strand", "strand"], ["Species", "species"], ["Domain", "domain"], ["Replicon", "replicon"], ["Software", "program_name"], ["Score", "score"], ["Align.", "alignment"], ["Run", "run"]]

    def __init__(self):
        """ Build an explore_model object defined by    
            data_manager(type:core.data_manager)   the application data manager  
        """
        self.data_manager = data_manager()
    
    def user_has_data(self, user_id, project_id):
        """ Return True if the user has data, false else 
            user_id(type:string)   the user id
        """
        return self.data_manager.user_has_project(user_id, project_id)
    
    def user_has_done_a_run(self, user_id, preoject_id):
        return self.data_manager.user_has_done_a_run(user_id, preoject_id)
    
    def get_putative_rnas(self, user, project_id = 0):
        return self.data_manager.get_putative_rnas(user, project_id)

    def filter_putative_rnas(self, filter, predictions):
        return filter.run(predictions)

    def sort_putative_rnas_by(self, arns, sort_by, ascent):
        table_to_return = []
        if sort_by == "start_position" or sort_by == "stop_position":
            tmp_table_id = []
            tmp_table = {}
            for i in range(len(arns)):
                if arns[i].get_x("genomic_sequence_id") not in tmp_table_id:
                    tmp_table_id.append(arns[i].get_x("genomic_sequence_id"))
                try:
                    tmp_table[arns[i].get_x("genomic_sequence_id")].append([arns[i].get_x(sort_by), i])
                except:
                    tmp_table[arns[i].get_x("genomic_sequence_id")] = []
                    tmp_table[arns[i].get_x("genomic_sequence_id")].append([arns[i].get_x(sort_by), i])
            tmp_table_id = sorted(tmp_table_id, key=operator.itemgetter(0))
            for i in tmp_table_id:
                tmp_sub_table = []
                for j in range(len(tmp_table[i])):
                    try:
                        tmp_sub_table.append([int(tmp_table[i][j][0]), tmp_table[i][j][1]])
                    except:
                        tmp_sub_table.append([tmp_table[i][j][0], tmp_table[i][j][1]])
                
                sub_table_sorted = sorted(tmp_sub_table, key=operator.itemgetter(0))    
                if not ascent:
                    for i in reversed(range(len(sub_table_sorted))):
                        table_to_return.append(arns[sub_table_sorted[i][1]])
                else:
                    for i in range(len(sub_table_sorted)):
                        table_to_return.append(arns[sub_table_sorted[i][1]])
        else:
            tmp_table = []
            for i in range(len(arns)):
                attributs_to_sort = arns[i].get_x(sort_by)
                if type(attributs_to_sort) == type([]):
                    attributs_to_sort = len(attributs_to_sort)
                try:
                    tmp_table.append([int(attributs_to_sort), i])
                except:
                    tmp_table.append([attributs_to_sort, i])
                
            sorted_table = sorted(tmp_table, key=operator.itemgetter(0))
            if not ascent:
                for i in reversed(range(len(sorted_table))):
                    table_to_return.append(arns[sorted_table[i][1]])
            else:
                for i in range(len(sorted_table)):
                    table_to_return.append(arns[sorted_table[i][1]])                   
        return table_to_return        

    def get_runs_info(self, user_id, project_id):
        ptrace = self.data_manager.get_project_trace(user_id, project_id)
        predict_events = ptrace.get_predict_events_for_display()
        result = {}
        for event in predict_events:
            try:
                result[event.run_id]["nb_total"] += int(event.nb_prediction)
                try:
                    result[event.run_id]["events"].append(event)
                except:
                    result[event.run_id]["events"] = []
                    result[event.run_id]["events"].append(event)
            except:
                result[event.run_id] = {}
                result[event.run_id]["nb_total"] = int(event.nb_prediction)
                result[event.run_id]["events"] = []
                result[event.run_id]["events"].append(event)
        return result

    def sort_and_filter_putative_rnas(self, arns, params, cookie=False):
        if cookie:
            old_filter = self.get_filter_from_cookie(params)
            filtered_arns = self.filter_putative_rnas(old_filter, arns)
            sorted_arns = self.sort_putative_rnas_by(filtered_arns, params["sort_by"].value, params["ascent"].value)
        else:
            old_filter = self.get_filter_from_params(params)
            filtered_arns = self.filter_putative_rnas(old_filter, arns)
            sorted_arns = self.sort_putative_rnas_by(filtered_arns, self.get_sort_by(params), self.get_sort_ascent(params))
        return sorted_arns

    def delete_putative_rnas(self, user_id, project_id, params):
        all_prnas = self.get_putative_rnas(user_id, project_id)        
        rnas_to_delete = self.__get_selected_putative_rnas(params)
        align_to_delete = []
        for prna in all_prnas:
            if prna.sys_id in rnas_to_delete:
                align_to_delete.extend(prna.alignment)
                
        for align in align_to_delete:
            self.data_manager.delete_alignment(user_id, project_id, align)
        self.data_manager.delete_putative_rnas(user_id, project_id, rnas_to_delete)
        e = remove_rna_event(user_id, project_id,
                             self.data_manager.get_user_email(user_id,project_id),
                             rnas_to_delete)
        self.data_manager.update_project_trace(user_id,project_id, [e])
    
    def create_export_file(self, user_id, project_id, all, params):
        format = self.__get_export_format(params)
        if all:
            rnas_to_export = self.data_manager.get_putative_rnas(user_id, project_id)
            rnas_id_to_export = []
            for r in rnas_to_export:
                rnas_id_to_export.append(r.user_id)
        else:
            rnas_id_to_export = self.__get_selected_putative_rnas(params)
            rnas_to_export = []
            for rna_id in rnas_id_to_export:
                rnas_to_export.append(self.data_manager.get_putative_rna(user_id, rna_id, project_id))

        e = export_event(user_id, project_id,
                         self.data_manager.get_user_email(user_id,project_id),
                         rnas_id_to_export,
                         format)
        self.data_manager.update_project_trace(user_id,project_id, [e])

        return self.data_manager.create_export_file(user_id, project_id, rnas_to_export, format)
        
    def get_action(self, params):
        if params.has_key("action"):
            return params["action"]
        else:
            return ""

    def get_show_allowed(self):
        return explore_model.show_allowed   
        
    def get_nb_criteria (self, params):
        if params.has_key("nb_criteria"):
            return params["nb_criteria"]
        else:
            return 0 
    
    def get_filter_from_params(self, params):
        f = filter()
        if params.has_key("nb_criteria"):
            for i in range(int(params["nb_criteria"])):
                cname = "criteria" + str(i)
                if cname != params["to_delete"]:
                    oname = "operators" + str(i)
                    vname = "value" + str(i)
                    c = selection_criteria(params[cname])
                    c.operator = params[oname]
                    c.value = (params[vname])
                    f.add_criteria(c)
            if self.get_action(params) == "add_criteria":
                if params["criteria"] != "-1":
                    cname = "criteria"
                    oname = "operators"
                    vname = "value"
                    c = selection_criteria(params[cname])
                    c.operator = params[oname]
                    c.value = (params[vname])
                    f.add_criteria(c)      
        return f

    def get_filter_from_cookie(self, cookie):
        f = filter()
        if cookie.has_key("nb_criteria"):
            for i in range(int(cookie["nb_criteria"].value)):
                cname = "criteria" + str(i)
                oname = "operators" + str(i)
                vname = "value" + str(i)
                c = selection_criteria(cookie[cname].value)
                c.operator = cookie[oname].value
                c.value = (cookie[vname].value)
                f.add_criteria(c)     
        return f

    def get_project_expiration_days(self):
        return self.data_manager.get_project_expiration_days()

    def get_filter_params(self, params):
        f = {}
        nb_criteria = 0
        if params.has_key("nb_criteria"):
            for i in range(int(params["nb_criteria"])):
                cname = "criteria" + str(i)
                if cname != params["to_delete"]:
                    f["criteria" + str(nb_criteria)] = params[cname]
                    f["operators" + str(nb_criteria)] = params["operators" + str(i)]
                    f["value" + str(nb_criteria)] = params["value" + str(i)]
                    nb_criteria += 1
            if self.get_action(params) == "add_criteria":
                if params["criteria"] != "-1":
                    f["criteria" + str(nb_criteria)] = params["criteria"]
                    f["operators" + str(nb_criteria)] = params["operators"]
                    f["value" + str(nb_criteria)] = params["value"] 
                    nb_criteria += 1
        f["nb_criteria"] =  nb_criteria
        return f

    def get_current_page(self, params):
        if params.has_key("current_page"):
            return params["current_page"]
        else:
            return 1
        
    def get_nb_putative_rnas_per_page(self, params):
        if params.has_key("nb_putative_rnas_per_page"):
            return params["nb_putative_rnas_per_page"]
        else:
            return explore_model.show_allowed[0] 
             
    def get_sort_by(self, params):
        if params.has_key("sort_by"):
            return params["sort_by"]
        else:
            return "start_position"

    def get_sort_ascent(self, params):
        if params.has_key("ascent"):
            return (params["ascent"] == "True")
        else:
            return "True"

    def get_attributs_to_show(self, display_mode):
        if display_mode == "all":
            return explore_model.all
        else:
            return explore_model.terse_set

    def get_all_attributs_name(self):
        return self.get_attributs_to_show("all")
        
    def get_display_mode(self, params):  
        if params.has_key("display_mode"):
            return params["display_mode"]
        else:
            return "terse_set"

    def get_project_sequences(self, user_id, project_id):
        """
        Return                the sequence ids the project
        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        """
        sequences = []        
        try:
            ids = self.data_manager.get_sequences_id(user_id, project_id)   
            for id in sorted(ids):
                sequences.append(self.data_manager.get_sequence(user_id, id, project_id))
        except:
            pass
        return sequences

    def get_project_sequences_header(self, user_id, project_id):
        """
        Return(string)        the header of the project sequences
        user_id(string)       the id of the connected user
        project_id(string)    the id of the project
        """
        headers = {}
        try:
            ids = self.data_manager.get_sequences_id(user_id, project_id)
            for id in ids:
                headers[id] = self.data_manager.get_sequence_header(user_id, project_id, id)
        except:
            pass
        return headers

    def get_ids_from_authkey(self, id):
        """
        id(sting)      the id containing the user_id and the project_id
        return [user_id, project_id]
        """
        return self.data_manager.get_ids_from_authkey(id)

    def get_authkey(self, user_id, project_id):
        """
        user_id(sting)      the user_id
        project_id(string)  the project_id
        return the id
        """
        return self.data_manager.get_authkey(user_id, project_id)

    def create_cgview_file(self, user_id, project_id, params):
        rnas_id_to_export = []
        for rna in range(int(params["nb_putative_rna"])):
            rnas_id_to_export.append(params["putative_rna"+str(rna)])
        
        rnas_to_export = []
        for rna_id in rnas_id_to_export:
            rna = self.data_manager.get_putative_rna(user_id, rna_id, project_id)
            rnas_to_export.append(rna)
        try:
            converter = cgview_converter()
            tmp_dir = self.data_manager.config.get("storage","tmp_dir")
            tmp_filename = os.path.basename(tempfile.NamedTemporaryFile().name)
            output =  os.path.join(tmp_dir, tmp_filename + '.tab')
            web_path = tmp_filename + '.tab'
            seq_length = len(self.data_manager.get_sequence(user_id, rnas_to_export[0].genomic_sequence_id, project_id))
            converter.write(rnas_to_export, seq_length, output)
            return web_path
        except:
            raise IOError, 'Error when attempting to create CGView file!'

    def tab_file_content(self, name):
        tmp_dir = self.data_manager.config.get("storage", "tmp_dir")
        path = os.path.join(tmp_dir, name)

        # protect the reading of other than image files in tmp_dir
        if os.path.dirname(path) != tmp_dir:
            return "Sorry, this file is not a tab file..."
        fpath = open(path, 'r')
        return fpath

    
    def __get_export_format(self, params):
        if params.has_key("export_format"):
            return params["export_format"]
        else:
            return ""

    def __get_selected_putative_rnas(self, params):
        selected = []
        if params.has_key("nb_checkbox"):
            for i in range(int(params["nb_checkbox"])):
                name = "checkbox" + str(i)
                if params.has_key(name):
                    selected.append(params[name])
        return selected
        
    def is_an_authentification_platform(self):
        return self.data_manager.is_an_authentification_platform()
    
    def get_mount_point(self):
        return self.data_manager.get_mount_point()

    
