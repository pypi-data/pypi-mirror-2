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

import math

from rnaspace.core.putative_rna import putative_rna
from rnaspace.core.alignment import alignment
from rnaspace.core.alignment import alignment_entry
from rnaspace.core.id_tools import id_tools

def __simple_merge(alignments, max_shift, strand):

    if len(alignments) == 0:
        return([], [])

    merged = []    
    merged.append(alignments[0])
    not_merged = [[alignments[0]]]

    k = 0
    for (i, a) in enumerate(alignments[1:]):
        ref_begin = a.ref_begin
        ref_end = a.ref_end
        db_begin = a.db_begin
        db_end = a.db_end
        currentref_begin = merged[k].ref_begin
        currentref_end = merged[k].ref_end
        currentdb_begin = merged[k].db_begin
        currentdb_end = merged[k].db_end
        if math.fabs((currentref_begin - currentdb_begin) - 
                     (ref_begin - db_begin)) < max_shift:
            not_merged[k].append(a)
            merged[k].ref_begin = min(currentref_begin, ref_begin)
            merged[k].ref_end = max(currentref_end, ref_end)
            merged[k].db_begin = min(currentdb_begin, db_begin)
            merged[k].db_end = max(currentdb_end, db_end)
            merged[k].evalue = min(float(merged[k].evalue), float(a.evalue))
        else:
            k = k + 1
            merged.append(a)
            not_merged.append([a])

    return (merged, not_merged)


def merge(family, alignments, max_shift, db_name, user_id, project_id, run_id,
          seq, program_name, program_version, day, month, year, max_ali):

    compat_strands = {"-":[("+", "-"), ("-", "+")], 
                      "+":[("+", "+"), ("-", "-")]}

    prnas_to_add = []
    alignments_to_add = []
    
    sorted_alignments = {"-":[], "+":[]}

    # classify alignments by strands
    for (i, a) in enumerate(alignments):
        if (a.ref_strand, a.db_strand) in compat_strands["-"]:
            sorted_alignments["-"].append(a)
        elif (a.ref_strand, a.db_strand) in compat_strands["+"]:
            sorted_alignments["+"].append(a)
            
    (mplus, nmplus) = __simple_merge(sorted_alignments["+"], max_shift, "+")
    (mminus, nmminus) = __simple_merge(sorted_alignments["-"], max_shift, "-")

    (rnas, align) = build_results(mplus, nmplus, family, alignments, max_shift, 
                                  user_id, project_id, run_id, seq, 
                                  program_name, program_version, day, month, 
                                  year, "+", max_ali)
    prnas_to_add.extend(rnas)
    alignments_to_add.extend(align)
    (rnas, align) = build_results(mminus, nmminus, family, alignments, 
                                  max_shift, user_id, project_id, run_id, seq, 
                                  program_name, program_version, day, month, 
                                  year, "-", max_ali)

    prnas_to_add.extend(rnas)
    alignments_to_add.extend(align)

    return (prnas_to_add, alignments_to_add)


def get_complement(base):
    """ 
    Return the complement base
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
        'u': 'a',
        'n': 'n',
        'N': 'N'}
    return cbase_table[base]
 
def get_reverse_complement(seq):
    """ Return the reverse complement sequence
    seq(string)     the sequence to reverse and complement
    """
    rc_seq = ""
    for base in reversed(seq):
        rc_seq += get_complement(base)
    return rc_seq
    

def build_results(merged, not_merged, family, alignments, max_shift, user_id, 
                  project_id, run_id, seq, program_name, program_version, 
                  day, month, year, strand, max_ali):

    prnas_to_add = []
    alignments_to_add = []
    id_gen = id_tools()

    for (i, a) in enumerate(merged):            
        pid = "temp"
        if strand == "-":
            sequence = get_reverse_complement(seq.data[a.ref_begin:a.ref_end])
        else:
            sequence = seq.data[a.ref_begin:a.ref_end]
        prna = putative_rna(pid, seq.id, a.ref_begin, a.ref_end,
                            run_id, user_id=pid, family=family,
                            sequence=sequence,
                            domain=seq.domain, species=seq.species,
                            strain=seq.strain, replicon=seq.replicon,
                            score=a.evalue, strand=strand, 
                            program_name=program_name, 
                            program_version=program_version,
                            day=day, month=month, year=year,
                            alignment=[])

        try:
            index = prnas_to_add.index(prna)
            prna = prnas_to_add[index]
        except:            
            pid = id_gen.get_new_putativerna_id(user_id, project_id, seq.id)
            prna.sys_id = pid
            prna.user_id = pid
            prnas_to_add.append(prna)
        #tnot_merged = list(not_merged[i])
        not_merged[i].sort(cmp=lambda x,y: cmp(float(x.evalue), float(y.evalue)))
        for temp_a in not_merged[i][:int(max_ali)]:
            align_id = id_gen.get_new_alignment_id(user_id, project_id)
            
            a1 = alignment_entry(prna.sys_id, temp_a.ref_seq, temp_a.ref_begin,
                                 temp_a.ref_end, seq.id, None, seq.replicon,
                                 seq.domain, seq.species, seq.strain,
                                 a.ref_strand, "", family)
            a2 = alignment_entry(temp_a.db_seq_name, temp_a.db_seq,
                                 temp_a.db_begin, temp_a.db_end, temp_a.db_name,
                                 None, seq.replicon, seq.domain, seq.species,
                                 seq.strain, a.db_strand, "", family)
            
            if temp_a.score is not None:
                sc = temp_a.score
            else:
                sc = ""

            if temp_a.evalue is not None:
                ev = temp_a.evalue
            else:
                ev = ""

            if temp_a.pvalue is not None:
                pv = temp_a.pvalue
            else:
                pv = ""


            align = alignment(align_id, [a1, a2], run_id,
                              program_name=program_name,
                              program_version=program_version,
                              day=day, month=month, year=year, 
                              score=sc, evalue=ev, pvalue=pv)
            
            index = prnas_to_add.index(prna)
            prnas_to_add[index].alignment.append(align_id)
            alignments_to_add.append(align)
            
    return (prnas_to_add, alignments_to_add)


class align(object):

    def __init__(self, ref_begin, ref_end, db_begin, db_end, ref_seq, db_seq, 
                 db_name, db_seq_name, ref_strand, db_strand, score, full_name,
                 family_id, evalue=None, pvalue=None):
        self.ref_begin = ref_begin
        self.ref_end = ref_end
        self.db_begin = db_begin
        self.db_end = db_end
        self.ref_seq = ref_seq
        self.db_seq = db_seq
        self.db_name = db_name
        self.db_seq_name = db_seq_name
        self.ref_strand = ref_strand
        self.db_strand = db_strand
        self.score = score
        self.full_name = full_name
        self.family_id = family_id
        self.evalue = evalue
        self.pvalue = pvalue
    
    def __cmp__(self, other):
        if self.ref_begin == other.ref_begin:
            return cmp(self.ref_end, other.ref_end)
        else:
            return cmp(self.ref_begin, other.ref_begin)

    def __str__(self):
        return "[(" + str(self.ref_begin) + "," + str(self.ref_end) + ")" +\
            "-" + "(" + str(self.db_begin) + "," + str(self.db_end) + ")]" +\
            self.db_seq_name
