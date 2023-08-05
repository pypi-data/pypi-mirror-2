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

function explore(mount_point){
	$("#home_btn").attr("href", mount_point + "index?authkey=" + $("#authkey").val())
	$("#predict_btn").attr("href", mount_point + "predict/index?authkey=" + $("#authkey").val())
	$("#explore_btn").attr("href", mount_point + "explore/index?authkey=" + $("#authkey").val())
	$("#manage_btn").attr("href", "")
	$("#manage_btn").click(function() {
	    jConfirm("If you get back on this page, you will restart a brand new project, keep on going ?", 'Confirm', function(r) {
	      if ( r ) {
	        document.location.replace(mount_point + "manage")
	      }
	    });
	    return false;
	});
	$("#value").change(function() {
	    $("#current_page").val(1);
	    $("#action").val("add_criteria");
		$('#explore_form').submit();
	}).blur(function() {
		if ($(this).val() == "") {
			$(this).val("Give value")
		}
	}).focus(function() {
		if ($(this).val() == "Give value") {
			$(this).val("")
		}
	});
	$("#add_criteria").click(function() {
	    $("#current_page").val(1);
	    $("#action").val("add_criteria");
		$('#explore_form').submit();
	});
	$(":button[id|='update_criteria']").each(function() {
		$(this).click(function() {
		    $("#current_page").val(1);
		    $("#action").val("");
			$('#explore_form').submit();
		});
	});
	$(":button[id|='delete_criteria']").each(function() {
		$(this).click(function() {
		    $("#current_page").val(1);
		    $("#to_delete").val("criteria" + $(this).attr("name"));
		    $("#action").val("");
			$('#explore_form').submit();
		});
	});
	$("#display").change(function() {
	    $("#display_mode").val($(this).val());
	    $("#action").val("");
		$('#explore_form').submit();
	});
	$("#show").change(function() {
	    $("#nb_putative_rnas_per_page").val($(this).val());
		$("#current_page").val(1);
	    $("#action").val("");
		$('#explore_form').submit();
	});
	$('#select_all_none').click(function() {
		if ($("#all_none").html() == "All") {
			$("#all_none").html("None");
			$("input[type=checkbox]").attr('checked', true);
		} else {
			$("#all_none").html("All");
			$("input[type=checkbox]").attr('checked', false);
		}
		return false;
    });
	$("a.change_page").each(function() {
		$(this).click(function() {
		    $("#current_page").val($(this).attr("name"));
		    $("#action").val("");
			$('#explore_form').submit();
			return false;
		});
	});
	$("#change_from_text").change(function() {
		if (parseInt($(this).val()) > 0 && parseInt($(this).val()) <= parseInt($("#nb_page").val())) {
		    $("#current_page").val($(this).val());
		    $("#action").val("");
			$('#explore_form').submit();
		} else {
        	jAlert('Page number out of range [1-' + parseInt($("#nb_page").val()) + '].', 'Warning');
    	}
	});
	$("#select_export_all").change(function() {
        if ($("input:checkbox").size() < 1) {
			jAlert('None existing prediction', 'Warning');
	    } else {
			format = $(this).val();
	     	jConfirm('Export all RNAs ?', 'Confirm', function(r) {
	      		if ( r ) {
	        		$("#action").val("export_all");
	        		$("#export_format").val(format);
					$('#explore_form').submit();
	      		}
	    	});
	    }
	    $(this).val("export");
	});
	$("#select_export").change(function() {
		format = $(this).val();
		if($("input:checkbox:checked").size() > 0) {
		    if($(this).val() == 'apollo_gff' && !(allFromSame("genomic_sequence_id"))) {
		    	jAlert('Predictions have not been predicted on the same sequence!', 'Warning');
		    } else {
                        if($("input:checkbox:checked").size() > 5) {
		    	    msg = "Export the " + $("input:checkbox:checked").size() + " RNAs selected ?"
		        } else {
		    	    msg = "Export the following RNAs: "
		    	    $("input:checkbox:checked").each(function() {
		    		    msg += $(this).attr("id") + ", ";
		    	    });
		    	    msg = msg.substr(0,msg.length-2) + " ?";
		        }
	                jConfirm(msg, 'Confirm', function(r) {
	                  if ( r ) {
		            $("#action").val("export");
		            $("#export_format").val(format);
		            $('#explore_form').submit();
	                  }
	                });
                    }
		} else {
			jAlert('No predictions selected', 'Warning');
		}
		$(this).val("export");
	});
	$("#select_analyse").change(function() {
		if ($(this).val() == "alignment") {
			if($("input:checkbox:checked").size() > 1) {
	                    test_size = 1;
		                $("input:checkbox:checked").each(function(i){
	                            var par = $(this).parents("tr");
	                            var tds = $(par).find("td").eq(6);
	                            var size = parseInt($(tds).text());
		                    if(size > 500){
	                                 test_size = 0;
	                            }
	                        });
	                        if(test_size == 1){
				    url = mount_point + "explore/alignment/index?authkey=" + $("#authkey").val() + "&";
				    $("input:checkbox:checked").each(function(i) {
		    		         url += "putative_rna" + i + "=" + $(this).val() + "&"
		                    });
		                    if($("input:checkbox:checked").size()>10){
		                        jAlert('Too much predictions selected (10 max)', 'Warning');
		                    }else{
		                        url += "nb_putative_rna=" + $("input:checkbox:checked").size()
		                        location.replace(url);
	                            }
	                        } else{
	                            jAlert('Some sequences are too long, alignment can not be performed', 'Warning');
	                        }
			} else {
				jAlert('Two predictions at least have to be selected', 'Warning');
			}
		}else if ($(this).val() == "cgview") {
			if($("input:checkbox:checked").size() > 0) {
				if (allFromSame("genomic_sequence_id")) {
		           	url = mount_point + "explore/get_cgview_file?authkey=" + $("#authkey").val() + "&";
					$("input:checkbox:checked").each(function(i) {
			    		     url += "putative_rna" + i + "=" + $(this).val() + "&"
			        });
			        url += "nb_putative_rna=" + $("input:checkbox:checked").size();
			    	$("#explore_dialog").dialog('option', 'title', 'CGView');
			    	$("#explore_dialog").dialog('option', 'width', 650);
			    	$("#explore_dialog").dialog('option', 'height', 650);
			    	$("#explore_dialog").dialog('option', 'position', 'top');
			    	$("#explore_dialog").html('<img src="'+mount_point+'ressource/img/light_wait.gif"/>').dialog("open");
		            $.ajax({
					  url: url,
					  success: function(val){
					    $("#explore_dialog").html("").dialog("open");
		            	var tab_url = mount_point + 'explore/tab_file?authkey=' + $("#authkey").val() + '&name=' + val;
					    $("#explore_dialog").html('<applet code="CGView.class" width="600" height="600" archive="'+mount_point+'ressource/applet/CGView.jar">  <param NAME="file" VALUE="' + tab_url + '">  <param NAME="hideLegend" VALUE="T"> <param NAME="rulerFontSize" VALUE="10"> </applet> ').dialog("open");
					  }
					});
				} else {
					jAlert('Predictions have not been predicted on the same sequence!', 'Warning');
				}
			} else {
				jAlert('One predictions at least have to be selected', 'Warning');
			}
        }
		$(this).val("analyse");
	});
	$("a.sort_table").each(function() {
		$(this).click(function() {
		    if($(this).attr("name") == $("#sort_by").val()) {
		    	if ($("#ascent").val() == "True") {
		    		$("#ascent").val("False")
		    	} else {
		    		$("#ascent").val("True")
		    	}
		    }
		    $("#sort_by").val($(this).attr("name"));
			$("#action").val($(this).attr(""));
			$('#explore_form').submit();
			return false;
		});
	});
	$(":select[id|='update_operator']").each(function() {
		$(this).change(function() {
			if ($(this).val() == "-1") {
				$("#"+$(this).attr("name")).html("<option value='-1'> Comparison </option>")
			} else {
				html = ""
				for (i=0; i<getAvailableCombinaison()[$(this).val()].length; i++) {
					html += "<option value='" + getAvailableCombinaison()[$(this).val()][i] + "'> " + getAvailableCombinaison()[$(this).val()][i] + "</option>"
				}
				$("#"+$(this).attr("name")).html(html)
			}
		});
	});
	$("#select_edition").change(function() {
		if ($(this).val() == "same_family") {
			if($("input:checkbox:checked").size() > 0) {
				url = mount_point + "explore/putinsamefamily/index?authkey=" + $("#authkey").val() + "&";
				$("input:checkbox:checked").each(function(i) {
		    		url += "putative_rna" + i + "=" + $(this).val() + "&"
		    	});
		    	url += "nb_putative_rnas=" + $("input:checkbox:checked").size()
		    	$("#explore_dialog").dialog('option', 'title', 'Rename Family');
	    		$("#explore_dialog").dialog('option', 'width', 300);
	    		$("#explore_dialog").dialog('option', 'height', 150);
	    		$("#explore_dialog").dialog('option', 'position', 'center');
		    	$("#explore_dialog").html('<img src="'+mount_point+'ressource/img/light_wait.gif"/>').dialog("open");
				$.ajax({
				  url: url,
				  success: function(html){
				    $("#explore_dialog").html(html).dialog("open");
					$("#put_form").putInSameFamily();
				  }
				});
			} else {
				jAlert('No predictions selected', 'Warning');
			}
		} else if ($(this).val() == "split") {
			if($("input:checkbox:checked").size() > 1) {
				url = mount_point+"explore/splitinto2families/index?authkey=" + $("#authkey").val() + "&";
				$("input:checkbox:checked").each(function(i) {
		    		url += "putative_rna" + i + "=" + $(this).val() + "&"
		    	});
		    	url += "nb_putative_rnas=" + $("input:checkbox:checked").size()
		    	$("#explore_dialog").dialog('option', 'title', 'Split into 2 families');
	    		$("#explore_dialog").dialog('option', 'width', 750);
	    		$("#explore_dialog").dialog('option', 'height', 250);
	    		$("#explore_dialog").dialog('option', 'position', 'center');
		    	$("#explore_dialog").html('<img src="'+mount_point+'ressource/img/light_wait.gif"/>').dialog("open");
				$.ajax({
				  url: url,
				  success: function(html){
				    $("#explore_dialog").html(html).dialog("open");
					$("#split_form").splitInto2Families();
				  }
				});
			} else {
				jAlert('Two predictions at least have to be selected', 'Warning');
			}
		} else if ($(this).val() == "add") {
		    location.replace(mount_point + "explore/rnavisualisation/index?authkey=" + $("#authkey").val() + "&mode=creation");
		} else if ($(this).val() == "merge") {
		    if($("input:checkbox:checked").size() > 1) {
		    	if (allFromSame("genomic_sequence_id")) {
		    		if (allFromSameStrand()) {
				  	  	url = mount_point + "explore/rnavisualisation/index?authkey=" + $("#authkey").val() + "&mode=merge&";
			        	$("input:checkbox:checked").each(function(i) {
			    			url += "putative_rna" + i + "=" + $(this).val() + "&"
			    		});
			    		url += "nb_putative_rnas=" + $("input:checkbox:checked").size()
			        	location.replace(url);
			        }
			        else { jAlert('Predictions have not been predicted on the strand!', 'Warning'); }
			    } else { jAlert('Predictions have not been predicted on the same sequence!', 'Warning'); }
		    } else { jAlert('Two predictions at least have to be selected!', 'Warning'); }
		} else if ($(this).val() == "delete") {
			if($("input:checkbox:checked").size() > 0) {
			    if($("input:checkbox:checked").size() > 5) {
			    	msg = "Are you sure you want to delete the " + $("input:checkbox:checked").size() + " RNA(s) selected ?"
			    } else {
			    	msg = "Are you sure you want to delete the following prediction(s): "
			    	$("input:checkbox:checked").each(function() {
			    		msg += $(this).attr("id") + ", ";
			    	});
			    	msg = msg.substr(0,msg.length-2) + " ?";
			    }
			    jConfirm (msg, 'Confirm', function(r) {
		          if ( r ) {
		            $("#action").val("delete");
					$('#explore_form').submit();
		          }
		        });
			} else {
				jAlert('No predictions selected', 'Warning');
			}
		}
		$(this).val("edit");
	});

	function allFromSame(attribut) {
		var tmp = "";
		var ok = true;
		$("input[type=checkbox]").each(function(i) {
			if ($(this).attr('checked')) {
				if (tmp == "") {
					tmp = $("#"+attribut+i).html();
				}
				if (tmp != $("#"+attribut+i).html()) {
					ok = false;
				}
			}
		});
		return ok;
	}

	function allFromSameStrand() {
		var tmp  = "";
		var ok   = true;
		expr = new RegExp("[.]");
		$("input[type=checkbox]").each(function(i) {
			if ($(this).attr('checked')) {
				if (tmp == "" || expr.test(tmp) ) {
					tmp = $("#strand"+i).html();
				}
				if (!expr.test(tmp) && !expr.test($("#strand"+i).html()) && tmp != $("#strand"+i).html()) {
					ok = false;
				}
			}
		});
		return ok;
	}

	$(":a[id|='sequence_info']").each(function() {
		$(this).click(function() {
			$("#explore_dialog").dialog('option', 'title', 'Sequence visualisation');
	    	$("#explore_dialog").dialog('option', 'width', 750);
	    	$("#explore_dialog").dialog('option', 'height', 500);
	    	$("#explore_dialog").dialog('option', 'position', 'top');
	    	$("#explore_dialog").html('<img src="'+mount_point+'ressource/img/light_wait.gif"/>').dialog("open");
	    	url = mount_point + "explore/sequencevisualisation/index?authkey=" + $("#authkey").val() + "&sequence_id=" + $(this).attr("name")
			$.ajax({
			  url: url,
			  success: function(html){
			    $("#explore_dialog").html(html).dialog("open");
			  }
			});
			return false;
		});
	});

    $("#explore_dialog").dialog({
	    autoOpen: false,
        width: 750,
        bgiframe: true,
        resizable: false,
        position: 'center',
	    modal: true,
        overlay: {
            backgroundColor: '#000',
            opacity: 0.5
        }
    });
}