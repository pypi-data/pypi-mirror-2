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

from rnaspace.ui.view.popup_template import popup_template

class alignment_helper(popup_template):

    def get_complement(self, base):
        """ Return the complement base
        base(string)     the base to complement
        """
        cbase_table = {
            'A': 'T',
            'a': 't',
            'T': 'A',
            't': 'a',
            'C': 'G',
            'c': 'g',
            'G': 'C',
            'g': 'c',
            'U': 'A',
            'u': 'a'}
        
        try:
            return cbase_table[base]
        except KeyError:
            return ""
 

    def is_identical(self, nuc_a, nuc_b):
        a = nuc_a.lower()
        b = nuc_b.lower()
        identicals = {'u':['t', 'u'], 't':['t','u']}

        if a == b:
            return True

        if (b == 'u' or b == 't') and a in identicals[b]:
            return True

        return False
        
    def increment(self, val, inc, gaps):
        return val + inc - 2 - gaps
    
    def decrement(self, val, dec, gaps):
        return val - dec + 2 + gaps

    
    def print_rna_m(self, rna_m):

        if rna_m.nb_seq == 2:
            if len(rna_m.sequences[0].secondary) > 0:
                return self.print_html(rna_m)
                
            else:
                return self.print_html_on_2_seq(rna_m)
        else:
            return self.print_html(rna_m)


    def print_html_on_2_seq(self, rna_m):
        
        alignment = ""

        maxChar = 65
        nameSize = 15
        tabSize = 3
    
        rnaA = rna_m.sequences[0]
        if rnaA.begin > rnaA.end:
            opA = self.decrement
        else:
            opA = self.increment

        rnaB = rna_m.sequences[1]
        if rnaB.begin > rnaB.end:
            opB = self.decrement
        else:
            opB = self.increment

        previous_rnaA_end = rnaA.begin - 1
        previous_rnaB_end = rnaB.begin - 1 
        # primary structure
        for i in range(0, rnaA.size/maxChar + 1):
            begin = i*maxChar
            end = min(i*maxChar+maxChar, rnaA.size)
        
            # first RNA name
            for j in range(0, min(nameSize, len(rnaA.user_name))):
                alignment += rnaA.user_name[j]
            for k in range(j+1, nameSize + tabSize):
                alignment += ' '
            # first RNA sequence
            alignment += '%5d ' % (previous_rnaA_end + 1)
            for j in range(begin, end):
                alignment += '<span class="' + rnaA.color[j] + '">'
                if rnaA.primary[j] == 'u':
                    alignment += 't'
                elif rnaA.primary[j] == 'U':
                    alignment += 'T'
                else:
                    alignment += rnaA.primary[j]
                alignment += '</span>'
            alignment += ' %5d\n'%(opA(rnaA.begin, min(i*maxChar+maxChar, 
                                                       rnaA.size), 
                                       rnaA.primary.count('-', 0, end)-1))
            previous_rnaA_end = opA(rnaA.begin, min(i*maxChar+maxChar, 
                                                    rnaA.size),
                                    rnaA.primary.count('-', 0, end) - 1)
            # middle
            for k in range(0, nameSize + tabSize + 6):
                alignment += ' '
            for j in range(begin, end):
                if self.is_identical(rnaA.primary[j], rnaB.primary[j]):
                    alignment += '|'
                else:
                    alignment += ' '
            alignment += '\n'
            # second RNA name
            for j in range(0, min(nameSize, len(rnaB.user_name))):
                alignment += rnaB.user_name[j]
            for k in range(j+1, nameSize + tabSize):
                alignment += ' '
            alignment += '%5d ' % (previous_rnaB_end + 1)
            # second RNA sequence
            for j in range(begin, end):
                alignment += '<span class="' + rnaB.color[j] + '">'
                if rnaB.primary[j] == 'u':
                    alignment += 't'
                elif rnaB.primary[j] == 'U':
                    alignment += 'T'
                else:
                    alignment += rnaB.primary[j]
                alignment += '</span>'
            alignment += ' %5d\n'%(opB(rnaB.begin, min(i*maxChar+maxChar, 
                                                       rnaB.size), 
                                       rnaB.primary.count('-', 0, end)-1))
            previous_rnaB_end = opB(rnaB.begin, min(i*maxChar+maxChar, 
                                                    rnaB.size),
                                    rnaB.primary.count('-', 0, end) - 1)
            alignment += '\n'

        return alignment

    def print_html(self, rna_m):

        alignment = ""
    
        maxChar = 65
        nameSize = 15
        tabSize = 3

        # primary structure
        for i in range(0, rna_m.sequences[0].size/maxChar + 1):
            begin = i*maxChar
            end = min(i*maxChar+maxChar, rna_m.sequences[0].size)
            for seq in rna_m.sequences:
                # name
                for j in range(0, min(nameSize, len(seq.user_name))):
                    alignment += seq.user_name[j]
                for k in range(j+1, nameSize + tabSize):
                    alignment += ' '
                for j in range(begin, end):
                    alignment += '<span class="' + seq.color[j] + '">'
                    alignment += seq.primary[j]
                    alignment += '</span>'
                alignment += '\n'
            alignment += ' '*(nameSize+tabSize)
            alignment += rna_m.print_comment(rna_m.primary_comment,
                                             begin, end) 
            alignment += '\n\n'

        alignment += '\n\n'

        if len(rna_m.sequences[0].secondary) > 0:
            # secondary structure
            for i in range(0, rna_m.sequences[0].size/maxChar + 1):
                begin = i*maxChar
                end = min(i*maxChar+maxChar, rna_m.sequences[0].size)
                for seq in rna_m.sequences:                                
                    # name
                    for j in range(0, min(nameSize, len(seq.user_name))):
                        alignment += seq.user_name[j]
                    for k in range(j+1, nameSize + tabSize):
                        alignment += ' '
                    for j in range(begin, end):
                        alignment += '<span class="' + seq.color[j] + '">'
                        alignment += seq.secondary[j]
                        alignment += '</span>'
                    alignment += '\n'
                alignment += ' '*(nameSize+tabSize)
                alignment += rna_m.print_comment(rna_m.secondary_comment,
                                                 begin, end)
                alignment += '\n\n'


        return alignment


    def get_page_navigation(self, current_page, prna_id, authkey, nb_pages,
                            mount_point):
        """
        Return a html block to navigate between pages:
         
        < << [page_number] >> >

        """
        html = ""

        page = int(current_page)
        prev = page - 1
        next = page + 1

        base_url = mount_point+"explore/alignment?authkey=%s&amp;mode=display_all"
        prna_id_arg = "&amp;prna_id=%s" 
        page_number_arg = "&amp;page_number=%s"
        url = base_url + prna_id_arg + page_number_arg

        first_url = url % (authkey, prna_id, "1")
        prev_url  = url % (authkey, prna_id, str(prev))            
        next_url  = url % (authkey, prna_id, str(next))
        last_url  = url % (authkey, prna_id, nb_pages)

        link = '<a href="%s">%s</a>\n'
        first_link = link % (first_url, "&lt;&lt;")
        prev_link  = link % (prev_url, "&lt;")
        next_link  = link % (next_url, "&gt;")
        last_link  = link % (last_url, "&gt;&gt;")

        if page > 1:
            html += first_link + prev_link

        html += 'Page <select class="select change_from_text"'
        html += ' size="1">'
        for p in xrange(1, int(nb_pages) + 1):
            if p == page:
                html += '<option selected="selected">' + str(p) + '</option>'
            else:
                html += "<option>" + str(p) + "</option>"
        html += '</select>'
        html += ' of %s \n'%(nb_pages)

        if page < int(nb_pages):
            html += next_link + last_link

        return html


    def get_aligment_header(self, align_id, program, entries, rnas, score, 
                            evalue, pvalue):

        """
        Return information about the current alignment
        """

        html =  ' <div class="cbb_title">\n'        
        html += 'Alignment produced by %s</div>\n'%program
        html += '<div class="cbb_content"><br /><br /> \n'

        nb_entries = len(entries)
        has_struct = len(rnas.sequences[0].secondary) > 0 
        if nb_entries == 2 and not has_struct:
            html += '<span class="top-bot-sequence">Top sequence: </span>'
            html += 'RNA prediction %s <br />\n' % (rnas.sequences[0].user_name)
            html += '<span class="top-bot-sequence">Bottom sequence: </span>'
            for entry in entries:
                if entry.rna_id.startswith("%"):
                    end = min(len(rnas.sequences[1].user_name), 100)
                    html += entry.genomic_sequence_id[1:]   
                    html += ' %s<br />' %( rnas.sequences[1].user_name[1:end])
      
        if score != "":
            html += '<span class="align-score"> score</span>: ' + str(score)
      
        if evalue != "":
            html += '<span class="align-score"> E-value</span>: ' + str(evalue)

        if pvalue != "":
            html += '<span class="align-score"> P-value</span>: ' + str(pvalue)

        return html

    def split_db_user_sequences(self, aligns):
        """
        split user sequences and db sequences from all the alignments
        """

        user = {}
        db = {}

        for align_id in aligns:
            for prna in aligns[align_id]['entries']:
                if prna.rna_id[0] != '%':
                    user.setdefault(align_id, [])
                    user[align_id].append(prna)
                else:
                    db.setdefault(align_id, [])
                    db[align_id].append(prna)

        return (user, db)
            
