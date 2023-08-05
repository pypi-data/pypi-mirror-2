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

def get_checked(predictor, checked_softs):

    unchecked = '<input type="checkbox" name="%s_%s_name" />'
    checked = '<input type="checkbox" name="%s_%s_name" checked="checked" />'

    ptype = predictor.type.split('_')[0]
    
    if (checked_softs is None or ptype not in checked_softs or
        predictor.name not in checked_softs[ptype]):
        return unchecked%(predictor.name, ptype)
    else:
        return checked%(predictor.name, ptype)


def get_radio(predictor, selected, pos):


    s_radio = '<input type="radio" checked="checked" name="%s" value="%s" />%s'
    radio = '<input type="radio" name="%s" value="%s" />%s'

    if predictor.type == "conservation":
        name = 'cons_soft'
    elif predictor.type == "aggregation":
        name = 'agg_soft'
    else:
        name = 'inf_soft'

    if selected is not None:
        if predictor.name == selected[predictor.type]:
            return s_radio%(name, predictor.name, predictor.name)
        else:
            return radio%(name, predictor.name, predictor.name)
    elif pos == 0:
        return s_radio%(name, predictor.name, predictor.name)
    else:
        return radio%(name, predictor.name, predictor.name)


def get_name(predictor):

    name = '%s <span class="type_%s"><i>(%s)</i></span>'

    ptype = predictor.type.split('_')[0]

    if predictor.type == "known_homology":
        long_type = "sequence homology"
    elif predictor.type == "known_rna_motif":
        long_type = "RNA motif search"
    elif predictor.type == "known_specialized":
        long_type = "specialized"
    else:
        return predictor.name

    return name%(predictor.name, ptype, long_type)

def get_param_button_name(predictor):
    if predictor.type == "conservation":
        name = "param_button_conservation_" + predictor.name
    elif predictor.type == "aggregation":
        name = "param_button_aggregation_" + predictor.name
    else:
        name = "param_button_inference_" + predictor.name

    return name

def get_option(predictor, opt, updated):

    ptype = predictor.type.split('_')[0]

    try:
        up = updated[ptype][predictor.name]
    except:
        up = None

    option_name = "%s_%s_%s_option"%(opt, predictor.name, ptype)

    long_option = False

    checkbox = '<input type="checkbox" name="%s" />'%(option_name)
    s_checkbox = '<input type="checkbox" checked="checked" name="%s" />'
    s_checkbox = s_checkbox%(option_name)
    
    text_a = '<input class="customizeinput" type="text" name="%s"'
    text_a += ' size="%s" value="%s" />\n'

    s_radio = '<input type="radio" checked=checked name="%s" value="%s" />%s'
    radio = '<input type="radio" name="%s" value="%s" />%s'
    
    sel_option = '<option selected="selected">%s</option>\n'
    option = '<option>%s</option>\n'
    begin_select = '<select class="limited_width select" name="%s" size="1">\n'
    end_select = '</select>\n'

    if opt in predictor.long_options:
        long_option = True
        opt_view = predictor.options_view[opt]
        if opt_view.startswith("text"):
            try:
                (opt_view, opt_size) = opt_view.split(':')
            except:
                opt_size = 5
            
        if up is not None and opt in up:
            value = up[opt]
        else:
            value = predictor.options_default[opt]
    else:
        if up is not None:
            if opt in up:
                checked = True
            else:
                checked = False
        else:
            checked = opt in predictor.default_simple

    if long_option:
        if opt_view == "text area":
            res = text_a%(option_name, str(opt_size), value)
        elif opt_view == "listbox":
            res = begin_select%(option_name)
            for param in predictor.opts_param_flat[opt]:
                if value == param:
                    res += sel_option%(param)
                else:
                    res += option%(param)
            res += end_select            
        elif opt_view == "radio":
            res = ''
            for param in predictor.opts_param_flat[opt]:
                if value == param:
                    res += s_radio%(option_name, param, param)
                else:
                    res += radio%(option_name, param, param)
    else:
        if checked:
            res = s_checkbox
        else:
            res = checkbox

    return res


def get_number_options(predictor):

    long_options = 0
    simple_options = 0
    
    if predictor.long_options != ['']:
        long_options = len(predictor.long_options)
    if predictor.simple_options != ['']:
        simple_options = len(predictor.simple_options)

    return long_options + simple_options


def get_number_basic_options(predictor):

    if predictor.basic_options[0] != '':
        num = len(predictor.basic_options)
    else:
        num = 0

    if predictor.database == "1":
        num += 1

    return num

def get_max_number_options(predictors):

    maxopts = get_number_basic_options(predictors[0])
    
    for predictor in predictors[1:]:
        num = get_number_basic_options(predictor)
        if num > maxopts:
            maxopts = num

    return maxopts
