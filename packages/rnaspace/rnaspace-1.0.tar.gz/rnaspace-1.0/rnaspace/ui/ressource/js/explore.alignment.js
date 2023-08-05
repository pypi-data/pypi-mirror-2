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


function alignment(mount_point){

  var pattern = "rnavisualisation";
  var reg = new RegExp(pattern);
  var authkey = $("#authkey").attr("value");
  var explore_url = mount_point + "explore/index?authkey=" + authkey;

  if(opener != null && reg.exec(opener.location) == null){
    opener.location.replace(explore_url);
  }

  $("#back").click(function(){
    document.location.replace(explore_url);
    return false;
  });

  $(".change_from_text").change(function(){
    var prna_id = $("#prna_id").attr("value");
    var p = $(this).val();
    var url = mount_point + "explore/alignment?authkey=" + authkey;
    url += "&amp;prna_id=" + prna_id + "&amp;page_number=" + p;
    url += "&amp;mode=display_all";
    document.location.replace(url);
  });

  $(".alignment_save_b").click(function(){
    var i = 0;
    var id = $(this).attr("id");
    var params = "&amp;authkey=" + authkey + "&amp;alignment_to_save=" + id;
    params = "?action=save" + params;

    $(".alignment_save_b").each(function(){
      if(id != $(this).attr("id")){
        params += "&amp;alignment" + i.toString() + "=" + $(this).attr("id");
        i++;
      }
    });
    params += "&amp;nb_alignments=" + i.toString();
    document.location.replace(mount_point + "explore/alignment" + params);
  });

  $(":a[id='ss_img']").each(function() {
    $(this).click(function() {
      $("#alignment_visualisation_dialog").dialog('option',
						  'title',
						  $(this).attr("name"));
      $("#alignment_visualisation_dialog").html('<img src="' +
						$(this).attr("href") +
						'" />').dialog("open");
      return false;
    });
  });

  $("#alignment_visualisation_dialog").dialog({
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