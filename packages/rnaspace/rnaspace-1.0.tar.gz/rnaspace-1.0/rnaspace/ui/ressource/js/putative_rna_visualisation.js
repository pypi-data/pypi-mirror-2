/*
 * RNAspace: non-coding RNA annotation platform
 * Copyright (C) 2009  CNRS, INRA, INRIA, Univ. Paris-Sud 11
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * Gathers all jQuery functions related to the explore page
 */

function putative_rna_visualisation(mount_point) {
	$('span').tooltip();
	if ($('#error').val() != '') {
		jAlert($('#error').val(), "Warning")
	}
	$("#edit").click(function() { 
		$("#mode").val("edition")
		$('#rna_form').submit();
	});
	$("#cancel").click(function() {
		$("*").removeAttr("required")
		$("*").removeAttr("mask")
		$("#mode").val("display")
		$("#action").val("cancel_modification")
		$('#rna_form').submit();
	});
	$("#reset").click(function() {
		$("*").removeAttr("required")
		$("*").removeAttr("mask")
		$("#action").val("cancel_modification")
		$('#rna_form').submit();
	});
	$("#add_prediction").click(function() { 
		$("#action").val("add");
		$('#rna_form').submit();
		opener.location.replace(mount_point+"/explore/index?authkey="+$("#authkey").val())
	});
	$("#add_structure").click(function() {
		if ($("#new_structure").hasClass("invalidInput")) {
			jAlert("The structure you are attempting to add is invalid!", "Warning");
		} else {
			$("#action").val("addstructure")
			$('#rna_form').submit();
		}
	});
	$("#sequence_id").change(function() { 
		$("#current_sequence_id").val($(this).val())
		$('#rna_form').submit();
	});
	$(":button[id|='del_structure']").each(function() { 
		$(this).click(function() {
			$("#action").val("delstructure")
			$("#structure_to_delete").val($(this).attr("name"))
			$('#rna_form').submit();
		});
	});
	$(":button[id='del_alignment']").each(function() { 
		$(this).click(function() {
			$("#action").val("delalignment")
			$("#alignment_to_delete").val($(this).attr("name"))
			$('#rna_form').submit();
		});
	});
	$("#update").click(function() { 
		$("#action").val("update")
		$('#rna_form').submit();
	});
	$("#predict_ss").click(function() { 
		if (parseInt($("#rna_size").val()) > parseInt($("#max_rna_size_for_structure_prediction").val())) {
			jAlert("The prediction size is too long to get computed by a secondary structure tools! (max length allowed = " + $("#max_rna_size_for_structure_prediction").val() + ")", "Warning");
			return false;
		} else {
			$("#predictor").val($(this).attr("name"))
			$("#action").val("predict")
			$('#rna_form').submit();
			return false;
		}
	});
	$("#new_structure").keyup(function() { 
		var struct_tab = parseStructure($(this).val());
		if ($(this).val().length == parseInt($("#rna_size").val())) {
			if (struct_tab == -1) {
				$(this).addClass('invalidInput');
			} else { 
				$(this).removeClass('invalidInput');
			}
		} else {
			$(this).addClass('invalidInput');
		}
	});
	$("#save").click(function() {
		if ($("#Strand").val() != $("#original_strand").val()) {
			if (parseInt($("#original_nb_structures").val()) > 0 && parseInt($("#original_nb_alignments").val()) > 0) {
		        jConfirm("You modified the strand, if you keep on going all structures and alignments related to this prediction will be deleted !", "Warning", function(r) {
					if (r) {
						$("#mode").val("display")
						$("#action").val("save")
						$('#rna_form').submit();
						opener.location.replace(mount_point+"/explore/index?authkey="+$("#authkey").val())
					}
				});
			} else if (parseInt($("#original_nb_structures").val()) > 0) {
		        jConfirm("You modified the strand, if you keep on going all structures related to this prediction will be deleted !", "Warning", function(r) {
					if (r) {
						$("#mode").val("display")
						$("#action").val("save")
						$('#rna_form').submit();
						opener.location.replace(mount_point+"explore/index?authkey="+$("#authkey").val())
					}
				});
			} else if (parseInt($("#original_nb_alignments").val()) > 0) {
		        jConfirm("You modified the strand, if you keep on going all alignments related to this prediction will be deleted !", "Warning", function(r) {
					if (r) {
						$("#mode").val("display")
						$("#action").val("save")
						$('#rna_form').submit();
						opener.location.replace(mount_point+"explore/index?authkey="+$("#authkey").val())
					}
				});
			} else {
				$("#mode").val("display")
				$("#action").val("save")
				$('#rna_form').submit();
				opener.location.replace(mount_point+"explore/index?authkey="+$("#authkey").val())
			}
		} else {
			if (parseInt($("#Start").val()) != parseInt($("#original_start_position").val()) || parseInt($("#End").val()) != parseInt($("#original_stop_position").val())) {
				if (parseInt($("#original_nb_structures").val()) > 0) {
			        jConfirm("You modified start/end values, if you keep on going all alignments related to this prediction will be deleted !", "Warning", function(r) {
						if (r) {
							$("#mode").val("display")
							$("#action").val("save")
							$('#rna_form').submit();
							opener.location.replace(mount_point+"explore/index?authkey="+$("#authkey").val())
						}
					});
				} else {
					$("#mode").val("display")
					$("#action").val("save")
					$('#rna_form').submit();
					opener.location.replace(mount_point+"explore/index?authkey="+$("#authkey").val())
				}
			} else {
				$("#mode").val("display")
				$("#action").val("save")
				$('#rna_form').submit();
				opener.location.replace(mount_point+"explore/index?authkey="+$("#authkey").val())
			}	
		}
	});
	$("#update").click(function() {
		$("#action").val("update")
		$('#rna_form').submit();
	});	
	
    $("#back").click(function() {
		location.replace(mount_point+"explore/index?authkey="+$("#authkey").val())
	});	
	
	$('#rna_form').formValidation({
		alias		: 'id'
		,err_class	: 'invalidInput'
		,required	: 'required'
		,err_list	: true
		,callback	: function() {
			if ($("#action").val() == "cancel_modification") { return true; }
			if ($("#original_id").val() != $("#ID").val()) {
			
				names = $("#rna_names_already_used").val().split(",");
				exists = false;
				for (i=0; i<names.length; i++) {
					if ($("#ID").val() == names[i]) {
						exists = true;
					}
				}
				if (exists) {
					$("#ID").addClass('invalidInput');
					jAlert("Prediction's ID: " + $("#ID").val() + " already exists! Please choose another one.", "Warning");
					return false;
				}
			}
			if (parseInt($("#Start").val()) > parseInt($("#End").val())) {
				$("#Start").addClass('invalidInput');
				$("#End").addClass('invalidInput');
				jAlert("Start value has to be lower than end value !", "Warning");
				return false;
			} else if (parseInt($("#Start").val()) < 1) {
				$("#Start").addClass('invalidInput');
				jAlert("Start value cannot be lower than 1 !", "Warning");
				return false;
			} else if (parseInt($("#End").val()) > parseInt($("#genome_size").val())) {
				$("#End").addClass('invalidInput');
				jAlert("End value cannot be upper than the sequence lenght (" + $("#genome_size").val() + ") !", "Warning");
				return false;
			}	
		}
	});
	
	$(":a[id|='ss_img']").each(function() {
		$(this).click(function() {
			$("#rna_visualisation_dialog").dialog('option', 'title', $("#structure_description_"+$(this).attr("id")).val());
			$("#rna_visualisation_dialog").html('<img src="' + $(this).attr("href") + '" />').dialog("open");
			return false;
		});
	});
	
    $("#rna_visualisation_dialog").dialog({
	    autoOpen: false,
        width: 750,
        bgiframe: true,
        resizable: false,
        position: 'top', 
	    modal: true,
        overlay: {
            backgroundColor: '#000',
            opacity: 0.5
        }
    });
}