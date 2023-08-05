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


from rnaspace.core.trace.event import predict_event
    
class project_trace (object):
    """ 
    Store (list of events) and manage trace for a user project
    events(type:[event])      list of events to add in the trace
    """
    
    def __init__(self):
        self.events = []

            
    def add_events(self, events):
        """
        events(type:[event])      list of events to add in the trace
        """
        self.events.append(events)

    def get_events(self, event_type):
        """
        event_type(type:string)         the type of event wanted
        Returns(type:[events])          a table of events
        """
        events_type = []
        for event in self.events:
            if event_type == event.type:
                events_type.append(event)
        return events_type

    def get_errors_events(self, run_id):
        """
         Returns(type:[events])          a table of error events for a run_id
        """
        events_error = []
        for event in self.events:
            if "ERROR" in event.type:
                if event.run_id == run_id:
                    events_error.append(event)
        return events_error

    def get_predict_events_for_display(self):
        """
        return a list of predict_event such as there is just one
        predict_even for a comparative execution and per gene finder
        No take into account of several sequences
        Returns(type:[events])          a table of events
        """

        # build a dictionnary run_id:[predict events of the run]
        run_events = {}
        for e in self.events:
            if isinstance(e, predict_event):
                if run_events.has_key(e.run_id):
                    run_events[e.run_id].append(e)
                else:
                    run_events[e.run_id]=[e]

        # aggregate events: one for comparative, one per gene_finder
        displayed_events = []
        for r,events in run_events.items():
            comparative_events = [] # list of comparative events (tagged with "comparative...")
            aggreg_events = {}      # dict aggregation_tag : [predict events with the tag]
            for e in events:
                if e.aggregation_tag[0:11]=="comparative":
                    comparative_events.append(e)
                else:
                    if aggreg_events.has_key( e.aggregation_tag ):
                        aggreg_events[e.aggregation_tag].append(e)
                    else:
                        aggreg_events[e.aggregation_tag] = [e]

            #aggregate comparative events
            if len(comparative_events)!=0:
                nb_prediction = 0
                nb_alignment = 0
                name_align = ""
                name_aggreg = ""
                name_infer = "" 
                for e in comparative_events:
                    nb_prediction = nb_prediction + e.nb_prediction
                    nb_alignment = nb_alignment + e.nb_alignment
                    if e.aggregation_tag == "comparative_align":
                        name_align = e.gene_finder_name
                    else:
                        if e.aggregation_tag == "comparative_aggreg":
                            name_aggreg = e.gene_finder_name
                        else:
                            if e.aggregation_tag == "comparative_infer":
                                name_infer = e.gene_finder_name
                name = name_align +"/"+ name_aggreg +"/"+ name_infer
                e = comparative_events[0]
                displayed_events.append( predict_event(e.user_id, e.project_id, 
                                                       "-", e.run_id,
                                                       "-", name, "-", {}, "-", 
                                                       nb_prediction, nb_alignment,
                                                       0, 0,"comparative") )

            #aggregate other events by gene finder
            for g,events in aggreg_events.items():
               nb_prediction = 0
               nb_alignment = 0
               for e in events:
                   nb_prediction = nb_prediction + e.nb_prediction
                   nb_alignment = nb_alignment + e.nb_alignment
               e = events[0]
               displayed_events.append( predict_event(e.user_id, e.project_id, 
                                                      "-", e.run_id,
                                                      "-", e.gene_finder_name, "-", {},
                                                      "-", nb_prediction, nb_alignment,
                                                      0, 0, e.aggregation_tag) )
        return  displayed_events 
