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

(function($){
	/*
    * Split into 2 families jquery functions
    */
	$.fn.splitInto2Families = function(){

		this_form = $(this);

		$(this).find("#to_family_a").click(function() {
			$("#center option:selected").each(function() {
				$(this).clone().prependTo("#family_a").tooltip();
				$(this).remove();
			});
			return false;
		});
		$(this).find("#to_family_b").click(function() {
			$("#center option:selected").each(function() {
				$(this).clone().prependTo("#family_b").tooltip();
				$(this).remove();
			});
			return false;
		});
		$(this).find("#center option").tooltip();
		$(this).find("#from_family_a").click(function() {
			$("#family_a option:selected").each(function() {
				$(this).clone().prependTo("#center").tooltip();
				$(this).remove();
			});
			return false;
		});
		$(this).find("#from_family_b").click(function() {
			$("#family_b option:selected").each(function() {
				$(this).clone().prependTo("#center").tooltip();
				$(this).remove();
			});
			return false;
		});
		$(this).find("#family_a").dblclick(function() {
			$("#family_a option:selected").each(function() {
				$(this).clone().prependTo("#center").tooltip();
				$(this).remove();
			});
		});
		$(this).find("#family_b").dblclick(function() {
			$("#family_b option:selected").each(function() {
				$(this).clone().prependTo("#center").tooltip();
				$(this).remove();
			});
		});
		$(this).find("#save").click(function() {
			$('#split_form').submit()
			if ($('#split_form .invalidInput').size() == 0) {
				data_value = "authkey=" + $("#authkey").val() + "&action=split_into_2_families&nb_family1=" + $("#family_a option").size() + "&nb_family2=" + $("#family_b option").size() + "&"
				data_value += "family1_name=" + $("#family_a_value").val() + "&family2_name=" + $("#family_b_value").val() + "&"
				$("#family_a option").each(function(i) {
					data_value += "to_family_1_" + i + "=" + $(this).val() + "&"
				});
				$("#family_b option").each(function(i) {
					data_value += "to_family_2_" + i + "=" + $(this).val() + "&"
				});
				$.ajax({
				  url: $("#mount_point").val() + "explore/splitinto2families/index",
				  data: data_value,
				  success: function(html){
					  this_form.parent().dialog("close");
					  if(html == ''){
					      document.location.replace($("#mount_point").val() + "explore/index?authkey="+$("#authkey").val());
					  }
					  else{
					      this_form.parent().parent().parent().html(html);
					  }
				  }
				});
			}
		});
		$(this).find("#cancel").click(function() {
			this_form.parent().dialog("close");
		});
		$(this).formValidation({
			alias		: 'name'
			,err_class	: 'invalidInput'
			,required	: 'required'
			,err_list	: true
			,callback	: function() {
					if ($("#family_a option").size() == 0 && $("#family_b option").size() == 0) {
						$("#family_a").addClass("invalidInput");
						$("#family_b").addClass("invalidInput");
						jAlert("Please split some predictions!")
					} else if ($("#family_a option").size() == 0) {
						$("#family_a").addClass("invalidInput");
						jAlert("Please add some predictions into Family A!")
					} else if ($("#family_b option").size() == 0) {
						$("#family_b").addClass("invalidInput");
						jAlert("Please add some predictions into Family B!")
					}
					return false;
				}
		});
   	return this;
   };


	/*
    * Put in same family jquery functions
    */
	$.fn.putInSameFamily = function(){

		this_form = $(this);

		$(this).find("#save").click(function() {
			$('#put_form').submit();
			if ($('#put_form .invalidInput').size() == 0) {
				data_value = "authkey=" + $("#authkey").val() + "&action=put_in_same_family&family=" + $("#family").val() + "&"
				$("input[id=putative_rna]").each(function(i) {
		    		data_value += "putative_rna" + i + "=" + $(this).val() + "&"
		    	});
		    	data_value += "nb_putative_rnas=" + $("input[id=putative_rna]").size();
				$.ajax({
				  url: $("#mount_point").val() + "explore/putinsamefamily/index",
				  data: data_value,
				  success: function(html){
					    this_form.parent().dialog("close");
					    if(html == ''){
						document.location.replace($("#mount_point").val() + "explore/index?authkey="+$("#authkey").val())
					    }
					    else{
						this_form.parent().parent().parent().html(html);
					    }
				  }
				});
			}
		});

		$(this).find("#cancel").click(function() {
			this_form.parent().dialog("close");
		});

		$(this).formValidation({
			alias		: 'name'
			,err_class	: 'invalidInput'
			,required	: 'required'
			,err_list	: true
			,callback	: function() { return false; }
		});

   	return this;

   }

})(jQuery)