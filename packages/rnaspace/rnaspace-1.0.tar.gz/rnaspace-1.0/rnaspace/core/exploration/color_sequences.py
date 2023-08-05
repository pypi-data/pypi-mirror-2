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
import os

NAME_SIZE = 20
NAME_TAB = 5
default_color = "blanc"

colors = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
          'aa', 'ba', 'ca', 'da', 'ea', 'fa', 'ga', 'ha', 'ia', 'ja', 'ka',
          'la', 'ma', 'na', 'oa', 'pa', 'qa', 'ra', 'sa', 'ta', 'ua', 'va',
          'wa', 'xa', 'ya', 'za']
max_color = len(colors)

###############################################################################
## RNA OBJECTS

class rna:
    
    """
    RNA object :
    \t name      : the name of the sequence
    \t primary   : the primary structure of the molecule
    \t secondary : the secondary structure
    \t partner   : array of partners
    \t color     : color for each nucleotide
    \t size      : size of the sequence
    """
    
    def __init__(self, name_tab, prim = "", sec = "",
                 eq = [], begin=0, end=0, user_name=""):
        self.name = name_tab
        if user_name == "":
            self.user_name = name_tab
        else:
            self.user_name = user_name
        self.primary = prim
        self.secondary = sec
        self.partner = []
        self.color = []
        self.size = len(self.primary)
        self.eq = eq
        self.begin = begin
        self.end = end


    def __init_color(self):
        """ 
        set the color as default_color for each position or compute color tab
        if eq files
        
        """
        for i in range(0, self.size):
            self.color.append(default_color)

        if len(self.eq) > 0:
            for i in range(self.size):
                if self.eq[i] < 0:
                    color = (-1 * self.eq[i]) % max_color
                    self.color[i] = colors[color]
                elif self.eq[i] > 0:
                    color = self.eq[i] % max_color
                    self.color[i] = colors[color]


    def __retrace_partner(self):
        """ 
        retrace partner for each nucleotide of sequence
        if a nucleotide is not paired, its partner is itself
        """
        stack = []
        for i in range(0, self.size):
            self.partner.append(i)
            
        for i in range(0, self.size):
            if self.secondary[i] == '(':
                stack.append(i)
            elif self.secondary[i] == ')':
                x = stack.pop()
                self.partner[i] = x
                self.partner[x] = i
            elif self.secondary[i] == '.' or self.secondary[i] == '-':
                self.partner[i] = i


    def init_all(self):
        self.size = len(self.primary)
        if len(self.secondary) > 0:
            self.__retrace_partner()
        self.__init_color()


    def __cmp__(self, other):
        return cmp(self.name, other.name)


    def __str__(self):
        info =  self.name + " size: " + str(self.size) + "\n"
        info = info + self.primary + "\n"
        info = info + self.secondary + "\n"
        info = info + str(self.partner) + "\n"
        info = info + str(self.color) + "\n"
        info = info + str(self.eq) + "\n"
        return info



class rna_multiple:
    
    """
    A list of RNA objects:
    \t nb_seq            : number of sequences
    \t sequences         : the list of sequences
    
    If the sequences are aligned:
    \t primary_comment   : a line of additionnal information about the primary 
    structure: tuple => (char, color)
    \t secondary_comment : a line of additionnal information about the 
    secondary structure: tuple => (char, color)
    \t superpairing      : the common secondary structure
    \t superpartner      : array of partners for the secondary structure
    """

    def __init__(self, list):
        """ list : a list of rna objects """
        self.sequences = list
        self.nb_seq = len(list)
        self.superpairing = []
        self.superpartner = []
        self.primary_comment = []
        self.secondary_comment = []


    def compute_super(self):
        """
        compute the superpairing and superpartner elements.
        """

        for i in range(0, self.sequences[0].size):
            self.superpairing.append('.') 
            self.superpartner.append(i)
            for seq in self.sequences:
                if seq.secondary[i] == '(' or seq.secondary[i] == ')':
                    self.superpairing[i] = seq.secondary[i]
                    self.superpartner[i] = seq.partner[i]


    def super_has_crossing_arcs(self):
        stack = []    
        try:
            for i in range(0, self.sequences[0].size):
                if self.superpairing[i] == '(':
                    stack.append(i)
                elif self.superpairing[i] == ')':
                    x = stack.pop()
            return len(stack) > 0
        except:
            return True

                    
    def gap_between(self, i, i_minus_one):
        j = self.superpartner[i]

        for seq in range(self.nb_seq):
            if self.sequences[seq].secondary[i] == '(':
                break
        x = i-1
        test = True
        while ( x > 0 and self.sequences[seq].secondary[x] != '(' and
                test == True):
            if self.sequences[seq].secondary[x] != '-':
                test = False
            x = x - 1            
        if test:
            j_plus_one = self.superpartner[x]
        else:
            j_plus_one = self.superpartner[i_minus_one]
            
        if j_plus_one > j:       
            for seq in range(self.nb_seq):
                if self.sequences[seq].secondary[j] != ')':
                    break          
            for x in range(j+1, j_plus_one):
                if self.sequences[seq].secondary[x] != '-':
                    return False                
            return True
        else:
            return False

    def gap_between_on_sequence(self, seq, i):
        j = seq.partner[i]
        i_minus_one = i-1
        x = i_minus_one
        test = True
        while ( x > 0 and seq.secondary[x] != '(' and
                test == True):
            if seq.secondary[x] != '-':
                test = False
            x = x - 1            
        if test:
            j_plus_one = seq.partner[x]
        else:
            j_plus_one = seq.partner[i_minus_one]

        if j_plus_one > j:                   
            for x in range(j+1, j_plus_one):
                if seq.secondary[x] != '-':
                    return False                
            return True
        else:
            return False

    def get_new_color(self, cols):
        for (i, color) in enumerate(colors):
            if i not in cols:
                return i
        return 0

    def compute_color_with_crossing_arcs(self):
        color_id = -1
        color_tab = {}
        for seq in self.sequences:
            for i in range(seq.size):
                if not (seq.secondary[i] == '.' or seq.secondary[i] == '-'):
                    j = seq.partner[i]
                    if i < j:
                        try:
                            current = color_tab[i][j]
                            seq.color[i] = colors[current]
                            seq.color[j] = colors[current]
                        except:
                            if not(i>0 and j<seq.size and 
                                   (seq.partner[i-1] == j+1 or
                                    self.gap_between_on_sequence(seq, i)) ):
                                color_id = (color_id + 1)%max_color
                                
                            seq.color[i] = colors[color_id]
                            seq.color[j] = colors[color_id]
                            color_tab.setdefault(i, {})
                            color_tab[i][j] = color_id

    def compute_color(self):
        """
        assign a color to each positions of each sequences
        """

        if self.super_has_crossing_arcs():
            self.compute_color_with_crossing_arcs()
            return
        current_color = -1        
        for i in range(0, self.sequences[0].size):
            if not (self.superpairing[i] == '.'):
                j = self.superpartner[i]
                if j > i :                    
                    if not (i > 0 and j < self.sequences[0].size and
                            (self.superpartner[i-1] == j+1 or
                             self.gap_between(i, i-1)) ):
                        current_color = (current_color + 1)%max_color

                    for seq in self.sequences:
                        if seq.secondary[i] == '(' or seq.secondary[i] == ')':
                            seq.color[i] = colors[current_color]
                            seq.color[j] = colors[current_color]
                            if (seq.secondary[j] == '-' or 
                                seq.secondary[j] == '.'):
                                self.compute_color_with_crossing_arcs()
                                return


    def compute_comment(self):
        """ 
        fill the comment line for the primary structure and
        the secondary structure
        """

        for i in range(0, self.sequences[0].size):
            conserve = 1
            c = self.sequences[0].primary[i]
            for seq in range(1, self.nb_seq):
                if self.sequences[seq].primary[i] != c:
                    conserve = 0
            if conserve:
                self.primary_comment.append(('*','noir'))
                self.secondary_comment.append((c,'noir'))
            else:
                self.primary_comment.append((' ','noir'))
                self.secondary_comment.append((' ','noir'))


    def __look_for(self, pattern, pattern_length):
        """
        look for pattern in the alignment
        pattern must be a compiled regular expression
        """        
        i = 0
        pos = []
        while i < self.sequences[0].size-(pattern_length-1):
            wxyz = ""
            for seq in self.sequences:
                for j in range(pattern_length):
                    wxyz = wxyz + seq.primary[i+j]
            if ( pattern.search(wxyz) ):                
                test = 1
                for j in range(pattern_length):
                    if self.superpairing[i+j] != '.':
                        test = 0
                if test:
                    left = i
                    right = i
                    while left > 0 and self.superpairing[left] != '.':
                        left = left - 1
                    while (right < self.sequences[0].size
                           and self.superpairing[right] != '.'):
                        right = right + 1
                    if (self.superpairing[left] != '(' and
                        self.superpairing[right] != ')'):
                        temp_pos = []
                        for j in range(pattern_length):
                            temp_pos.append(i+j)
                        pos.append( tuple(temp_pos) )
                        
            i = i + 1
            
        return pos


    def look_for_gnra(self, color):
        
        pattern = '(g[uagct][ag]a){%i}'%(self.nb_seq)
        gnra = re.compile(pattern)
        pos = self.__look_for(gnra, 4)        
        for (i, j, k, l) in pos:
            self.primary_comment[i] = ('G', color)
            self.primary_comment[j] = ('N', color)
            self.primary_comment[k] = ('R', color)
            self.primary_comment[l] = ('A', color)
            self.secondary_comment[i] = ('G', color)
            self.secondary_comment[j] = ('N', color)
            self.secondary_comment[k] = ('R', color)
            self.secondary_comment[l] = ('A', color)
                        

    def print_list(self, list, begin, end):
        s = ""
        for i in range(begin, end):
            s = s + list[i] 
        return s

            
    def print_comment(self, list, begin, end):
        s = ""
        for i in range(begin, end):
            (comment, col) = list[i]
            if col is 'rouge':
                s = s + '<font color="red">' + comment + '</font>'
            else:
                s = s + comment
        return s


    def print_superpairing(self):
        """ display superpairing in string format """
        pair = ""
        for c in self.superpairing:
            pair = pair + c
        return pair
   

    def __str__(self):
        info = ""
        for seq in self.sequences:
            info = info + str(seq) + "\n"
        info = info + self.print_superpairing() + "\n"
        info = info + str(self.superpartner)
            
        return info



###############################################################################
## INPUT FUNCTIONS


def get_color(file):
    return get_input_file(file, "fasta")

def read_file(file):
    """ read a file securely and return its data """

    try:
        fsock = open(file, "r")
        try:
            fdata = fsock.read()
        finally:
            fsock.close()
    except (IOError, TypeError):
        try:
            fdata = file.read()
        except:
            print "[!!] error reading file " + file
            if not os.path.isfile(file):
                print "\t file does not exist"
            exit(0)
    return fdata


def get_input_file(input, type):
    """ read the input files and return a list of RNA elements """
    list = []
        
    try:
        get_func = globals()["get_%s" % type]
    except AttributeError:
        print "[EE] format " + type + " is not supported"
        exit(0)

    rna_m = get_func(input)
    
    return rna_m


def get_fasta(file):
    """ read fasta file """
    data = read_file(file)
   #  data = valid_fasta_sequence(data)
#     if data is None:
#         print '[EE] file "' + file + '" is not in fasta format'
#         exit(1)

    data = data.splitlines()
    k = 0
    list = []
    for line in data:
        seqorstruc = re.sub(r'[-\.]','', line)
        if re.search('^ *>', line) is not None:
            #list.append(rna(line.replace(">", "")))
            list.append(rna(str(k), user_name=line.replace(">", "")))
            k = k + 1
        elif re.search('[atcguATCGU]+', seqorstruc) is not None:
            list[k-1].primary = list[k-1].primary + line
#        elif re.search('[()]+', seqorstruc) is not None:
        else:
            list[k-1].secondary = list[k-1].secondary + line
        
    for r in list:
        r.init_all()

    rna_m = rna_multiple(list)
        
    return rna_m


def valid_fasta_sequence(seq):
    """ check the validity of the fasta file """

    pattern =  """
        ^                                   # beginning of string
        (                                   # one sequence 
        \ *>.+[\r\n]+                       # line of the name
        ([-\.\ NATCGUatcgun0-9]+[\r\n]+)+   # line of the primary structure
        ([-\.\ \(\)]+[\r\n]+)*              # line of the secondary structure
        )                                   # end of one sequence
        {1,}$                               # at least two sequences
        """
    list_seq = seq.splitlines()
    temp_seq = ''
        
    # remove spaces for non-title line
    for x in list_seq:
        if re.search('^ *>', x) is None:
            x = x.lower()
            x = x.strip()
        temp_seq = temp_seq + x + '\n'
        
    essai = re.search(pattern, temp_seq, re.VERBOSE)
    if  essai is None:
        return None
    else:
        return seq

