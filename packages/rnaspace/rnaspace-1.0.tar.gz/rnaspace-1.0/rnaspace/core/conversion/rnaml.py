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
import re
import xml
from xml.dom.minidom import parse
from xml.dom.minidom import Document

from rnaspace.core.putative_rna import putative_rna
from rnaspace.core.secondary_structure import secondary_structure
from rnaspace.core.alignment import alignment
from rnaspace.core.alignment import alignment_entry
from alignment_to_rnaml import alignment_to_rnaml
from fixed_write_xml import fixed_writexml

# replace minidom's function with ours
xml.dom.minidom.Element.writexml = fixed_writexml

class rnaml (object):
    """ Class rnaml: converts objects to rnaml or read rnaml to objects
        This object has to be used as following:
            my_var = rnaml()
            my_var.read(path/to.rnaml.xml)
            obj = my_var.get_object()
    """   

    def __init__(self):
        self.alignment = alignment_to_rnaml()
    
    def write(self, obj, output):
        """ 
        writes a table of object into an rnaml file
        prnas(type:[putative_rna])  the putative_rna table to write down
        output(type:string)         path to the folder to store the rnaml file
        """
        if len(obj) > 0:
            if type(obj[0]) == putative_rna or isinstance(obj[0], putative_rna):
                self.__write_putative_rnas(obj, output)
            elif type(obj[0]) == alignment or isinstance(obj[0], alignment):
                self.alignment.write_alignment(obj, output)
            else: raise TypeError( str(type(obj)) + " is not supported by our rnaml converter.")
    
    # TODO: check the rnaml file against the xsd
    def read(self, path):
        self.path = path
        self.xmldoc = parse(path)
       
    def __get_root_element(self):
        if self.current_node == None:
            self.current_node = self.xmldoc.documentElement
        return self.current_node 
 
    def get_alignment(self):
        """ Return(type:alignment)   an alignment defined by the rnaml file
        """
        
        # catch the alignment attributs
        self.current_node = None
        properties = {}
        for align in self.__get_root_element().getElementsByTagName("alignment"):
            if align.nodeType == align.ELEMENT_NODE:
                try:
                    alignment_id = align.attributes["id"].nodeValue
                    for i in range(len(align.getElementsByTagName("molecule-id"))):
                        try:
                            m_id = align.getElementsByTagName("molecule-id")[i].childNodes[0].nodeValue
                            m_val = align.getElementsByTagName("seq-data")[i].childNodes[0].nodeValue
                            properties[m_id] = {}
                            properties[m_id]["sequence"] = m_val
                            s_format = align.getElementsByTagName("secondary-structure")[i].childNodes[1].childNodes[0].nodeValue
                            s_struct = align.getElementsByTagName("secondary-structure")[i].childNodes[3].childNodes[0].nodeValue
                            properties[m_id]["structure"] = secondary_structure(format=s_format, structure=s_struct)
                        except:
                            pass
                except:
                    pass

        # catch the consensus attributs
        self.current_node = None
        consensus = None
        for align in self.__get_root_element().getElementsByTagName("consensus-molecules"):
            if align.nodeType == align.ELEMENT_NODE:
                try:
                    consensus_sequence = align.getElementsByTagName("seq-data")[0].childNodes[0].nodeValue
                    consensus_sequence = consensus_sequence.strip()
                    structures = []
                    try:
                        consensus_structure = align.getElementsByTagName("ss-value")[0].childNodes[0].nodeValue
                        consensus_structure = consensus_structure.strip()
                        consensus_format = align.getElementsByTagName("ss-format")[0].childNodes[0].nodeValue
                        ss = secondary_structure(consensus_format, consensus_structure)
                        structures.append(ss)
                    except:
                        pass
                    consensus = putative_rna("consensus", "None", -1, -1, "None", sequence=consensus_sequence, structure=structures)
                except:
                    pass
        
        # catch the molecule-class attributs
        self.current_node = None
        prnas = []

        for align in self.__get_root_element().getElementsByTagName("molecule-class"):
            if align.nodeType == align.ELEMENT_NODE:
                try:
                    putative_rna_sys_id = align.getElementsByTagName("molecule")[0].attributes["id"].nodeValue
                    putative_rna_user_id = align.getElementsByTagName("name")[1].childNodes[0].nodeValue
                    putative_rna_size = int(align.getElementsByTagName("sequence")[0].attributes["length"].nodeValue)
                    putative_rna_genomic_sequence_id = align.getElementsByTagName("numbering-system")[0].attributes["id"].nodeValue
                    putative_rna_start = int(align.getElementsByTagName("start")[0].childNodes[0].nodeValue)
                    putative_rna_stop = int(align.getElementsByTagName("end")[0].childNodes[0].nodeValue)

                    try:
                        putative_rna_family = align.getElementsByTagName("name")[0].childNodes[0].nodeValue
                    except:
                        putative_rna_family = "unknown"
                    try:
                        putative_rna_replicon_value = re.search("REPLICON=(.*)", align.getElementsByTagName("taxonomy")[0].attributes["comment"].nodeValue)
                        putative_rna_replicon = putative_rna_replicon_value.group(1)
                    except:
                        putative_rna_replicon = ""
                    try:
                        putative_rna_domain = align.getElementsByTagName("domain")[0].childNodes[0].nodeValue
                    except:
                        putative_rna_domain = ""
                    try:
                        putative_rna_species = align.getElementsByTagName("species")[0].childNodes[0].nodeValue
                    except:
                        putative_rna_species = ""
                    try:
                        putative_rna_strand = align.getElementsByTagName("sequence")[0].attributes["strand"].nodeValue
                    except:
                        putative_rna_strand = ""
                    
                    properties[putative_rna_sys_id]["genomic_sequence_id"] = putative_rna_genomic_sequence_id
                    properties[putative_rna_sys_id]["start"] = long(putative_rna_start)
                    properties[putative_rna_sys_id]["stop"] = long(putative_rna_stop)
                    properties[putative_rna_sys_id]["family"] = putative_rna_family
                    properties[putative_rna_sys_id]["replicon"] = putative_rna_replicon
                    properties[putative_rna_sys_id]["species"] = putative_rna_species
                    properties[putative_rna_sys_id]["strand"] = putative_rna_strand
                    properties[putative_rna_sys_id]["domain"] = putative_rna_domain
                    properties[putative_rna_sys_id]["user_id"] = putative_rna_user_id
                except:
                    pass



        # catch the analysis attributs                
        self.current_node = None
        for align in self.__get_root_element().getElementsByTagName("analysis"):
            if align.nodeType == align.ELEMENT_NODE:
                try:
                    alignment_run = align.attributes["id"].nodeValue
                    try:
                        alignment_program_name = align.getElementsByTagName("prog-name")[0].childNodes[0].nodeValue  
                    except:
                        alignment_program_name = ""
                    try:
                        alignment_program_version = align.getElementsByTagName("prog-version")[0].childNodes[0].nodeValue  
                    except:
                        alignment_program_version = ""
                    try:
                        alignment_score = align.getElementsByTagName("score")[0].childNodes[0].nodeValue  
                    except:
                        alignment_score = ""
                    try:
                        alignment_evalue = align.getElementsByTagName("evalue")[0].childNodes[0].nodeValue  
                    except:
                        alignment_evalue = ""
                    try:
                        alignment_pvalue = align.getElementsByTagName("pvalue")[0].childNodes[0].nodeValue  
                    except:
                        alignment_pvalue = ""
                    try:
                        alignment_day = align.getElementsByTagName("day")[0].childNodes[0].nodeValue  
                        alignment_month = align.getElementsByTagName("month")[0].childNodes[0].nodeValue                 
                        alignment_year = align.getElementsByTagName("year")[0].childNodes[0].nodeValue  
                    except:
                        alignment_day = ""
                        alignment_month = ""
                        alignment_year = ""
                except:
                    pass

        alignment_entries = []
        for rna_id in properties:
            val = properties[rna_id]
            try:
                struc = val["structure"]
            except:
                struc = None
            a = alignment_entry(rna_id, val["sequence"], val["start"], val["stop"],
                                val["genomic_sequence_id"], struc, val["replicon"],
                                val["domain"], val["species"], "", val["strand"], val["user_id"],
                                val["family"])
            alignment_entries.append(a)

        align_to_return = alignment(alignment_id, alignment_entries, alignment_run, consensus,
                                    alignment_program_name, alignment_program_version,
                                    alignment_day, alignment_month, alignment_year, alignment_score, alignment_evalue, alignment_pvalue)
        return align_to_return

    def get_putative_rna(self):
        """ Return(type:putative_rna)   a putative_rna defined by the rnaml file
        """
        # catch the molecule-class attributs
        self.current_node = None
        for rna in self.__get_root_element().getElementsByTagName("molecule-class"):
            if rna.nodeType == rna.ELEMENT_NODE:
                try:

                    putative_rna_sys_id = rna.getElementsByTagName("molecule")[0].attributes["id"].nodeValue
                    try:
                        putative_rna_user_id = rna.getElementsByTagName("name")[1].childNodes[0].nodeValue 
                    except:
                        putative_rna_user_id = rna.getElementsByTagName("name")[0].childNodes[0].nodeValue 
                    putative_rna_size = int(rna.getElementsByTagName("sequence")[0].attributes["length"].nodeValue)
                    putative_rna_genomic_sequence_id = rna.getElementsByTagName("numbering-system")[0].attributes["id"].nodeValue
                    putative_rna_start = int(rna.getElementsByTagName("start")[0].childNodes[0].nodeValue)
                    putative_rna_stop = int(rna.getElementsByTagName("end")[0].childNodes[0].nodeValue)

                    try:
                        if len(rna.getElementsByTagName("name")) == 1:
                            putative_rna_family = "unknown"
                        else:
                            putative_rna_family = rna.getElementsByTagName("name")[0].childNodes[0].nodeValue
                    except:
                        putative_rna_family = "unknown"
                    try:
                        putative_rna_replicon_value = re.search("REPLICON=(.*)", rna.getElementsByTagName("taxonomy")[0].attributes["comment"].nodeValue)
                        putative_rna_replicon = putative_rna_replicon_value.group(1)
                    except:
                        putative_rna_replicon = ""
                    try:
                        putative_rna_domain = rna.getElementsByTagName("domain")[0].childNodes[0].nodeValue
                    except:
                        putative_rna_domain = ""
                    try:
                        putative_rna_species = rna.getElementsByTagName("species")[0].childNodes[0].nodeValue
                    except:
                        putative_rna_species = ""
                    try:
                        putative_rna_strain = rna.getElementsByTagName("strain")[0].childNodes[0].nodeValue
                    except:
                        putative_rna_strain = ""
                    try:
                        putative_rna_strand = rna.getElementsByTagName("sequence")[0].attributes["strand"].nodeValue
                    except:
                        putative_rna_strand = ""
                    try:
                        putative_rna_sequence = rna.getElementsByTagName("seq-data")[0].childNodes[0].nodeValue
                    except:
                        putative_rna_sequence = ""
                    try:
                        structure_table = []
                        for i in range(len(rna.getElementsByTagName("str-annotation"))):
                            structure_brackets_structure = rna.getElementsByTagName("str-annotation")[i].childNodes[0].nodeValue  
                            structure_predictor = rna.getElementsByTagName("method")[i].childNodes[0].nodeValue  
                            structure_free_energy = rna.getElementsByTagName("free-energy")[i].childNodes[0].nodeValue  
                            #TODO: to modify
                            s = secondary_structure("brackets", structure_brackets_structure, structure_predictor, structure_free_energy)
                            structure_table.append(s)                                                                  
                    except:
                        structure_table = []

                except:
                    raise IOError("The rnaml : " + self.path + " doesn't have molecule ids, it cannot be read by the system")

        alignments = []
        # catch the alignment attributs                
        self.current_node = None
        for rna in self.__get_root_element().getElementsByTagName("alignment"):
            if rna.nodeType == rna.ELEMENT_NODE:
                try:
                    alignments.append(rna.attributes["id"].nodeValue)
                except:
                    pass 
                    
        # catch the analysis attributs                
        self.current_node = None
        for rna in self.__get_root_element().getElementsByTagName("analysis"):
            if rna.nodeType == rna.ELEMENT_NODE:
                try:
                    putative_rna_run = rna.attributes["id"].nodeValue   
                    try:
                        putative_rna_score_value = re.search("SCORE=(.*)", rna.getElementsByTagName("program")[0].attributes["comment"].nodeValue)
                        putative_rna_score = float(putative_rna_score_value.group(1))                                                                  
                    except:
                        putative_rna_score = 0.0
                    try:
                        putative_rna_program_name = rna.getElementsByTagName("prog-name")[0].childNodes[0].nodeValue  
                    except:
                        putative_rna_program_name = ""
                    try:
                        putative_rna_program_version = rna.getElementsByTagName("prog-version")[0].childNodes[0].nodeValue  
                    except:
                        putative_rna_program_version = ""
                    try:
                        putative_rna_day = rna.getElementsByTagName("day")[0].childNodes[0].nodeValue  
                        putative_rna_month = rna.getElementsByTagName("month")[0].childNodes[0].nodeValue                 
                        putative_rna_year = rna.getElementsByTagName("year")[0].childNodes[0].nodeValue  
                    except:
                        putative_rna_day = ""
                        putative_rna_month = ""
                        putative_rna_year = ""
                except:
                    raise IOError("The rnaml : " + self.path + " doesn't have molecule ids, it cannot be read by the system")
               
        # then build and return the putative_rna
        prna =  putative_rna(putative_rna_sys_id, putative_rna_genomic_sequence_id, putative_rna_start, putative_rna_stop,
                             putative_rna_run, putative_rna_user_id, putative_rna_sequence, putative_rna_family, 
                             putative_rna_strand, putative_rna_domain, putative_rna_species, putative_rna_strain, putative_rna_replicon,
                             structure_table, putative_rna_score, putative_rna_program_name, putative_rna_program_version, putative_rna_day, 
                             putative_rna_month, putative_rna_year, alignments)
        return prna
    
    def __write_putative_rnas(self, prnas, output):
        """ writes a table of putative_rna into an rnaml file
            prnas(type:[putative_rna])  the putative_rna table to write down
            output(type:string)         path to the folder to store the rnaml file
        """
        xml = Document()
        rnaml = xml.createElement("rnaml")
        rnaml.setAttribute("version", "1.1")
        xml.appendChild(rnaml)
        
        for prna in prnas:
        
            molecule_class = xml.createElement("molecule-class")           
            rnaml.appendChild(molecule_class)                                  
            
            if prna.family != "unknown":
                identity_class = xml.createElement("identity")
                molecule_class.appendChild(identity_class)                
                name_class = xml.createElement("name")
                name_class.appendChild(xml.createTextNode(prna.family))  
                identity_class.appendChild(name_class)                 
            
            molecule = xml.createElement("molecule")
            molecule.setAttribute("type", "rna")
            molecule.setAttribute("id", prna.sys_id)
            molecule_class.appendChild(molecule)       
            
            identity = xml.createElement("identity")
            molecule.appendChild(identity)                
            name = xml.createElement("name")
            name.appendChild(xml.createTextNode(prna.user_id))
            identity.appendChild(name)
            
            if prna.replicon != "" or prna.domain != "" or prna.species != "":
                taxonomy = xml.createElement("taxonomy")
                if prna.replicon != "":
                    taxonomy.setAttribute("comment", "REPLICON=" + prna.replicon)
                identity.appendChild(taxonomy)
                if prna.domain != "":
                    domain = xml.createElement("domain")
                    domain.appendChild(xml.createTextNode(prna.domain))
                    taxonomy.appendChild(domain)
                if prna.species != "":
                    species = xml.createElement("species")
                    species.appendChild(xml.createTextNode(prna.species))
                    taxonomy.appendChild(species)
                if prna.strain != "":
                    strain = xml.createElement("strain")
                    strain.appendChild(xml.createTextNode(prna.strain))
                    taxonomy.appendChild(strain)
                    
            sequence = xml.createElement("sequence")
            sequence.setAttribute("length", str(prna.size))
            sequence.setAttribute("strand", prna.strand)  
            molecule.appendChild(sequence)                       
            numbering_system = xml.createElement("numbering-system")
            numbering_system.setAttribute("id", prna.genomic_sequence_id)
            sequence.appendChild(numbering_system)          
            numbering_range = xml.createElement("numbering-range")
            numbering_system.appendChild(numbering_range)
            start = xml.createElement("start")
            start.appendChild(xml.createTextNode(str(prna.start_position)))             
            numbering_range.appendChild(start) 
            end = xml.createElement("end")
            end.appendChild(xml.createTextNode(str(prna.stop_position)))            
            numbering_range.appendChild(end)
            seq_data = xml.createElement("seq-data")
            seq_data.appendChild(xml.createTextNode(prna.sequence))
            sequence.appendChild(seq_data) 
    
            if len(prna.structure) > 0:
                structure = xml.createElement("structure")                      
                molecule.appendChild(structure)
                model = xml.createElement("model") 
                structure.appendChild(model)
        
                # For each structures of the putative_rna
                for structs in prna.structure:
                    str_annotation = xml.createElement("str-annotation")
                    str_annotation.appendChild(xml.createTextNode(structs.structure))
                    model.appendChild(str_annotation)      
        
                    model_info = xml.createElement("model-info")
                    model.appendChild(model_info)           
                    method = xml.createElement("method")
                    method.appendChild(xml.createTextNode(structs.predictor))
                    model_info.appendChild(method)
                    free_energy = xml.createElement("free-energy")
                    free_energy.appendChild(xml.createTextNode(str(structs.free_energy)))
                    model_info.appendChild(free_energy)               
            
            if len(prna.alignment) > 0:
                for a in prna.alignment:
                    alignment = xml.createElement('alignment')
                    alignment.setAttribute('id', str(a))
                    rnaml.appendChild(alignment)
    
            if prna.program_name != "" or prna.program_version != "":
                analysis = xml.createElement("analysis")
                analysis.setAttribute("id", prna.run)
                rnaml.appendChild(analysis)                
                program = xml.createElement("program")
                program.setAttribute("comment", "SCORE=" + str(prna.score))
                analysis.appendChild(program)  
                if prna.program_name != "":
                    prog_name = xml.createElement("prog-name")
                    prog_name.appendChild(xml.createTextNode(prna.program_name))
                    program.appendChild(prog_name)  
        
                if prna.program_version != "":                          
                    prog_version = xml.createElement("prog-version")
                    prog_version.appendChild(xml.createTextNode(prna.program_version))    
                    program.appendChild(prog_version) 
            
            if prna.day != "" or prna.month != "" or prna.year != "":
                date = xml.createElement("date")
                analysis.appendChild(date) 
                if prna.day != "":   
                    day = xml.createElement("day")
                    day.appendChild(xml.createTextNode(prna.day))
                    date.appendChild(day)                 
                if prna.month != "":
                    month = xml.createElement("month")
                    month.appendChild(xml.createTextNode(prna.month))
                    date.appendChild(month)   
                if prna.year != "":
                    year = xml.createElement("year")
                    year.appendChild(xml.createTextNode(prna.year))
                    date.appendChild(year)          
            
            revision = xml.createElement("revision")
            rnaml.appendChild(revision)                                      
            revision_date = xml.createElement("date")
            revision.appendChild(revision_date)    
            revision_day = xml.createElement("day")
            revision_day.appendChild(xml.createTextNode(str(time.localtime()[2])))  
            revision_date.appendChild(revision_day)                 
            revision_month = xml.createElement("month")
            revision_month.appendChild(xml.createTextNode(str(time.localtime()[1])))  
            revision_date.appendChild(revision_month)   
            revision_year = xml.createElement("year")
            revision_year.appendChild(xml.createTextNode(str(time.localtime()[0])))  
            revision_date.appendChild(revision_year)  

        f = open(output, "w")
        xml.writexml(f, addindent='  ', newl='\n')
        f.close()
