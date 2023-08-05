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

import xml
from xml.dom.minidom import Document

from fixed_write_xml import fixed_writexml

# replace minidom's function with ours
xml.dom.minidom.Element.writexml = fixed_writexml

class alignment_to_rnaml:
    """
    Class to convert alignment object to rnaml and vice et versa
    """   


    def __text(self, element, text, xml):
        """
        return a text node
        """
        e = xml.createElement(str(element))
        t = xml.createTextNode(str(text))
        e.appendChild(t)

        return e

    def write_alignment(self, alis, output):
        """
        Write an alignment into a rnaml file
        
        alis([core.alignment])       the alignment object
        output(string)               the rnaml file path
        """
        
        xml = Document()
        rnaml = xml.createElement("rnaml")
        rnaml.setAttribute("version", "1.1")

        for ali in alis:

            for rna in ali.rna_list:
                # write sequences informations
                molecule_class = self.__get_molecule_class(rna, xml)
                rnaml.appendChild(molecule_class)

            # create alignment node
            alignment = self.__get_alignment(ali, xml)        
            rnaml.appendChild(alignment)

            consensus = self.__get_consensus(ali, xml)
            if consensus is not None:
                rnaml.appendChild(consensus)
            rnaml.appendChild(self.__get_analysis(ali, xml))
            rnaml.appendChild(self.__get_revision(xml))

        xml.appendChild(rnaml)

        fres = open(output, 'w')
        xml.writexml(fres, addindent=' ', newl='\n')
        fres.close()



    ############################################################################
    ## DESCRIPTION OF EACH SEQUENCE
    ##

    def __get_molecule_class(self, rna, xml):
        """
        Return <molecule-class> element

        prna(putative_rna)
        xml(xml.dom.minidom.Document)
        """
        
        molecule_class = xml.createElement('molecule-class')
        identity = self.__get_identity(rna.family, xml)
        molecule = self.__get_molecule(rna, xml)
        molecule_class.appendChild(identity)
        molecule_class.appendChild(molecule)

        return molecule_class

    def __get_identity(self, family, xml):
        """
        Return <identity> element
        """

        identity = xml.createElement('identity')
        identity.appendChild(self.__text('name', family, xml))

        return identity

    def __get_molecule(self, rna, xml):
        """
        Return a <molecule> element
        """
        
        molecule = xml.createElement("molecule")
        molecule.setAttribute("type", "rna")
        molecule.setAttribute("id", rna.rna_id)

        mol_identity = self.__get_mol_identity(rna, xml)
        sequence = self.__get_sequence(rna, xml)
        
        if mol_identity is not None:
            molecule.appendChild(mol_identity)
        molecule.appendChild(sequence)

        return molecule

    def __get_mol_identity(self, rna, xml):
        """
        Return a <identity> element
        """
        identity = xml.createElement('identity')
        identity.appendChild(self.__text('name', rna.user_id, xml))
        
        if (rna.replicon != "" or rna.domain != "" or rna.species != ""): 
            
            taxonomy = xml.createElement('taxonomy')
            if rna.replicon != "":
                taxonomy.setAttribute('comment', 'replicon=' + rna.replicon)

            if rna.domain != "":
                taxonomy.appendChild(self.__text('domain', rna.domain, xml))
            if rna.species != "":
                taxonomy.appendChild(self.__text('species', rna.species, xml))

            identity.appendChild(taxonomy)
        
        return identity

    def __get_sequence(self, rna, xml):
        """
        Return a <sequence> element
        """

        sequence = xml.createElement('sequence')
        sequence.setAttribute('length', str(rna.size))
        if rna.strand != '':
            sequence.setAttribute('strand', rna.strand)

        numbsys = xml.createElement('numbering-system')
        numbsys.setAttribute('id', rna.genomic_sequence_id)
        numbrange = xml.createElement('numbering-range')
        start = self.__text('start', rna.start, xml)
        stop = self.__text('end', rna.stop, xml)
        numbrange.appendChild(start)
        numbrange.appendChild(stop)
        numbsys.appendChild(numbrange)
        sequence.appendChild(numbsys)
        
        return sequence



    ############################################################################
    ## DESCRIPTION OF THE ALIGNMENT
    ##

    def __get_alignment(self, ali, xml):
        """
        Return <ali-sequence> element
        """

        alignment = xml.createElement("alignment")
        alignment.setAttribute("id", ali.id)

        for rna in ali.rna_list:
            ali_sequence = xml.createElement('ali-sequence')
            ali_sequence.appendChild(self.__text('molecule-id', rna.rna_id,
                                                 xml))
            ali_sequence.appendChild(self.__text('seq-data', rna.sequence, xml))
            if rna.structure is not None:
                secondary = xml.createElement('secondary-structure')
                s = rna.structure.structure
                f = rna.structure.format
                secondary.appendChild(self.__text('ss-format', f, xml))
                secondary.appendChild(self.__text('ss-value', s, xml))
                ali_sequence.appendChild(secondary)
            alignment.appendChild(ali_sequence)

        return alignment


    ############################################################################
    ## DESCRIPTION OF THE CONSENSUS
    ##

    def __get_consensus(self, ali, xml):
        """
        Return <consensus-molecules> element
        """
        if ali.consensus != None:
            consensus = xml.createElement('consensus-molecules')
            molecule = xml.createElement('molecule')
            molecule.setAttribute('type', 'rna')
            sequence = xml.createElement('sequence')
            sequence.appendChild(self.__text('seq-data', ali.consensus.sequence,
                                             xml))
            molecule.appendChild(sequence)
            if ali.consensus.structure != []:
                structure = xml.createElement('structure')
                model = xml.createElement('model')
                model_info = xml.createElement('model-info')
                ss = xml.createElement('secondary-structure')
                s = ali.consensus.structure[0].structure
                f = ali.consensus.structure[0].format
                ss.appendChild(self.__text('ss-format', f, xml))
                ss.appendChild(self.__text('ss-value', s, xml))
                model_info.appendChild(self.__text('method', ali.program_name,
                                                   xml))
                model.appendChild(ss)
                model.appendChild(model_info)
                structure.appendChild(model)
                molecule.appendChild(structure)
            consensus.appendChild(molecule)

            return consensus
        return None


    ############################################################################
    ## INFORMATION ABOUT THE ALIGNMENT GENERATION
    ##

    def __get_analysis(self, ali, xml):
        """
        Return <analysis> element
        """
        analysis = xml.createElement('analysis')
        analysis.setAttribute('id', ali.run_id)
        if ali.program_name != '':
            prog = xml.createElement('program')
            prog.appendChild(self.__text('prog-name', ali.program_name, xml))
            prog.appendChild(self.__text('prog-version', ali.program_version,
                                         xml))
            if ali.score != '':
                prog.appendChild(self.__text('score', ali.score, xml))
            if ali.evalue != '':
                prog.appendChild(self.__text('evalue', ali.evalue, xml))
            if ali.pvalue != '':
                prog.appendChild(self.__text('pvalue', ali.pvalue, xml))
            analysis.appendChild(prog)

        if ali.day != '' or ali.month != '' or ali.year != '':
            date = xml.createElement('date')
            if ali.day != '':
                date.appendChild(self.__text('day', ali.day, xml))
            if ali.month != '':
                date.appendChild(self.__text('month', ali.month, xml))
            if ali.year != '':
                date.appendChild(self.__text('year', ali.year, xml))
            analysis.appendChild(date)

        return analysis

    ############################################################################
    ## REVISIONS
    ##

    def __get_revision(self, xml):
        """
        Return <revision> element
        """
        revision = xml.createElement('revision')
        date = xml.createElement('date')
        date.appendChild(self.__text('day', str(time.localtime()[2]), xml))
        date.appendChild(self.__text('month', str(time.localtime()[1]), xml))
        date.appendChild(self.__text('year', str(time.localtime()[0]), xml))
        revision.appendChild(date)

        return revision
