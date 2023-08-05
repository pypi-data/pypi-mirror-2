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

function init_predict(mount_point){

  var
  manage_message = "If you get back on this page, you will restart " +
		     "a brand new project, keep on going ?",
  home_url = mount_point + "index?authkey="+$("#authkey").val(),
  predict_url = mount_point + "predict/index?authkey=" + $("#authkey").val(),
  manage_url = mount_point + "manage",
  explore_url = mount_point + "explore/index?authkey="+$("#authkey").val();


  /* set the tab links */
  $("#home_btn").attr("href", home_url);
  $("#predict_btn").attr("href", predict_url);
  $("#manage_btn").attr("href", manage_url);
  $("#manage_btn").click(back_to_manage);
  if($("#explore_btn").hasClass("notaccessible")){
    $("#explore_btn").attr("href", "");
    /* prevent browser from reloading the page */
    $("#explore_btn").click(function(){return false;});
  }
  else{
    $("#explore_btn").attr("href", explore_url);
  }

  function back_to_manage(){
    /* ask for confirmation before redirecting to manage page */
    jConfirm(manage_message, 'Confirm', function(r){
      if(r){
	document.location.replace(manage_url);
      }
    });
    return false;
  }


  /* Handle the parameters buttons */
  $("#parameters_dialog").dialog({
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

  $(".parameters_button").click(
    function(){
      var name = $(this).attr("name").split("_");
      var type = name[2];
      var soft = name[3];
      var key = $("#authkey").attr("value");
      var url = mount_point + "predict/parameters/index?authkey=" + key;

      url += "&amp;type=" + type;
      url += "&amp;softname=" + soft;
      $("#parameters_dialog").dialog('option', 'title',  soft + " settings");
      $.ajax({
	url: url,
	success: function(html){
	  $("#parameters_dialog").html(html).dialog("open");
	  $("#parameters_form").ajaxForm({success: showResponse});
	}
      });

      /* prevent default behaviour */
      return false;
    }
  );

  function showResponse(response, status){
    /* if some errors occured when submitting parameters */
    if(response != ""){
      $("#parameters_dialog").html(response);
      $("#parameters_form").ajaxForm({success: showResponse});
    }
    else{
      $("#parameters_form").resetForm();
      $("#parameters_dialog").dialog("close");
    }
  }



  /* Transform the species selection box in a single line box */
  $("#species_list").asmSelect({
				 addItemTarget: 'bottom',
				 animate: true,
				 highlight: true,
				 sortable: false
			       });


  /* Handle the "more" links to display a little help when clicked */
  $(".soft_description").css("display", "none");
  $(".toggle_help").click(
    function(){
      var parent = $(this).parent().parent().next(".soft_description");
      if(parent.length>0){
	$(this).parent().parent().next(".soft_description").toggle();
      }
      else{
	var next = $(this).parents("tr").next();
	$(next).children().children().show();
	$(next).toggle();
      }
      return false;
    });


  /* we validate the form before sending it to the server for a better user
   * experience.
   */
  $("#predict_submit").click(validate_form);
  function validate_form(){
    var checked = 0;

    $("div.check").each(
      function(){
	if($(this).children().attr("checked") == 1){
	  checked = checked + 1;
	}
      }
    );

    if( checked == 0 && $("#species_list").val() == null){
      jAlert("Please select a predictor.");
      return false;
    }

    if( $("#species_list").val().length > 5){
      jAlert("Too much species");
      return false;
    }
    return true;
  }
}