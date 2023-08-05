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

function manage(mount_point){

  var home_page = mount_point + "index?authkey=" + $("#authkey").val();
  var manage_page = mount_point + "manage/index?authkey=" + $("#authkey").val();
  var explore_page = mount_point + "explore/index?authkey="+$("#authkey").val();
  var predict_page = mount_point + "predict/index?authkey="+$("#authkey").val();
  var error_message = "Please fill all required fields ! (orange background)" +
			"<br /><ul><li>No sequence provided</li></ul>";

  $("#home_btn").attr("href", home_page);
  $("#manage_btn").attr("href", manage_page);
  if($("#explore_btn").hasClass("notaccessible")){
    $("#explore_btn").attr("href", "");
    $("#explore_btn").click(function(){return false;});
  }else{
    $("#explore_btn").attr("href", explore_page);
  }
  if($("#predict_btn").hasClass("notaccessible")){
    $("#predict_btn").attr("href", "");
    $("#predict_btn").click(function(){return false;});
  }else{
    $("#predict_btn").attr("href", predict_page);
  }

  $('#manage_form').formValidation({
    alias	: 'name',
    err_class	: 'invalidInput',
    required	: 'required',
    err_list	: true,
    callback	: function() {
      if($('#file').val() == "" && $('#sequences').val() == ""){
	$('#file').addClass("invalidInput");
	$('#sequences').addClass("invalidInput");
	jAlert(error_message, "Warning");
	return false;
      }
      return true;
    }
  });

  $('#submit_form').formValidation({
    alias	: 'name',
    err_class	: 'invalidInput',
    required	: 'required',
    err_message : 'Processing may be long, please provide a valid email !',
    err_list	: false,
    callback	: function() {}
  });

  $('#clear').click(function() {
    $('#id').val($('#seq_id').val());
    $('#id').removeClass('invalidInput');
    $('#domain').val("bacteria");
    $('#domain').removeClass('invalidInput');
    $('#file').val("");
    $('#file').removeClass('invalidInput');
    $('#sequences').val("");
    $('#sequences').removeClass('invalidInput');
    $('#species').val("unknown");
    $('#species').removeClass('invalidInput');
    $('#strain').val("unknown");
    $('#strain').removeClass('invalidInput');
    $('#replicon').val("unknown");
    $('#replicon').removeClass('invalidInput');
  });

  $('#sample').click(function() {
    window.location.href = manage_page + '&get_sample_sequence=True';
  });

  $('#add_sequence').click(function() {
    $('#action_manage').val('add_sequence');
    $('#manage_form').submit();
  });

  $('#configure_predictors').click(function() {
    $('#action_submit').val('configure_predictors');
    $('#submit_form').submit();
  });

  if ($('#error').val() != '') {
    jAlert($('#error').val(), "Warning");
  }
  if ($("#last_action").val() == "add_sequence") {
    window.location='#footer';
  }
  $("#predict_btn").attr("href", "#");
  $("#explore_btn").attr("href", "#");

  $('#id').focus(function() { $(this).val(''); });
  $('#id').blur(function() { $(this).val($('#current_seq_id').val()); });
  $('#species').focus(function() { $(this).val(''); });
  $('#species').blur(function() { $(this).val('unknown'); });
  $('#strain').focus(function() { $(this).val(''); });
  $('#strain').blur(function() { $(this).val('unknown'); });
  $('#replicon').focus(function() { $(this).val(''); });
  $('#replicon').blur(function() { $(this).val('unknown'); });
}
