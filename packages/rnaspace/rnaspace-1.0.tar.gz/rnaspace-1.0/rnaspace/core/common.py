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
import math

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

def __get_local_data(sums, dr, flst):
    for f in flst:
        fullf = os.path.join(dr,f)
        if os.path.islink(fullf): break
        if os.path.isfile(fullf):
            sums[0] += os.path.getsize(fullf)
            sums[1] += 1
        else:
            sums[2] += 1
    
def get_directory_info(dtroot):
    sums = [0,0,1]
    os.path.walk(dtroot, __get_local_data, sums)
    return sums[0]

def get_nb_octet(size):
    """
    Return the number of octet: value has to be formated like this: 5Mo, 20Go ...
    """
    octets_link = ["octets", "Ko", "Mo", "Go", "To", "Po", "Eo", "Zo"]
    unit = size[len(size)-2:len(size)]
    pow_val = int(octets_link.index(unit)) * 10
    val = pow(2, pow_val)
    nb_octet = int(size[:len(size)-2]) * val
    return nb_octet

def get_octet_string_representation(size):
    """
    Return the string representation of an octet
    """
    octets_link = ["octets", "Ko", "Mo", "Go", "To", "Po", "Eo", "Zo"]
    p = int(math.ceil(float(len(str(size)))/float(3) - float(1)))
    pow_needed = p * 10
    pow_needed = pow(2, pow_needed)
    value = str(float(size)/float(pow_needed))
    tmp = value.split(".")
    value = tmp[0] + "." + tmp[1][:2]
    try:
        value = value + " " + octets_link[p]
    except:
        raise TypeError("In core.common:project_id unexpected input value for size: " + str(size))
    return str(value)