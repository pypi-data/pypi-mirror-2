function help(){

  var num = 1;
  var subnum = 1;
  var subsubnum = 1;
  var winwidth = $(window).width();
  var containerwidth = $("#container").width();
  var diffwidth  = (winwidth - containerwidth)/2 + 750;

  build_toc();
  build_predictors_toc();


  if(/Firefox[\/\s](\d+\.\d+)/.test(navigator.userAgent)){
    var ffversion = new Number(RegExp.$1);
    if (ffversion>=3){
      $("#help_tocs").draggable({axis: "y"});
    }
    else{
      $("#help_tocs").bind('drag',
	function(event){
	  $(this).css({
			top:(event.offsetY-document.body.scrollTop),
			left:(event.offsetX-document.body.scrollLeft)
                      });
	}
      );
    }
  }
  else{
    $("#help_tocs").bind('drag',
      function(event){
	$(this).css({
		      top:(event.offsetY-document.body.scrollTop),
                      left:(event.offsetX-document.body.scrollLeft)
		    });
      }
    );
  }

  $("#help_tocs").fixedBox({x: diffwidth.toString(), y: "170"});

  $(".internal").click(
    function(){
      $.scrollTo("#help" + $(this).attr("id"), {speed: 500});
      return false;
    }
  );

  $(".internal-tmpl").live('click',
    function(){
      $.scrollTo($($(this).attr("href")), 500);
      return false;
    }
  );


  $("#help_predictors_toc_content a").click(
    function(){
      $.scrollTo($(this).attr("href"), {speed: 500});
      return false;
    }
  );

  // hide every subsections
  $(".slide_ul").slideToggle("normal");

  // we can hide the toc
  $("div#help_toc_title").click(
    function () {
      $("#help_toc_content").slideToggle("normal");
      return false;
    }
  );

  // we can hide the predictors toc
  $("div#help_predictors_toc_title").click(
    function () {
      $("#help_predictors_toc_content").slideToggle("normal");
      return false;
    }
  );

  // hide/show sections in toc
  $("span.slide").click(
    function(){
      $(this).next().children(".slide_ul").slideToggle("normal");
      if($(this).text() == " + "){
        $(this).text(" - ");
      }
      else{
        $(this).text(" + ");
      }
      return false;
    }
  );

  $(".help_soft_desc").click(
    function () {
      $(this).next(".help_soft_big_desc").slideToggle("normal");
      if($(this).children(".help_toggle_button").children().text() == "+"){
        $(this).children(".help_toggle_button").children().text("-");
      }else{
        $(this).children(".help_toggle_button").children().text("+");
      }
      return false;
    }
  );

  // build predictors toc
  function build_predictors_toc(){
    $("#help_predictors_toc_content").append('<ul id="help_predictors_toc_list"></ul>');
    $("div.help_soft_section").each(
      function(){
	var softname = $(this).attr("id");
	var li = "<li><a href=\"#" + softname + "\">" + softname + "</a></li>";
        $("#help_predictors_toc_list").append(li);
      }
    );
  }

  // build the toc
  function build_toc(){
    $("#help_toc_content").append('<ul id="help_toc_list"></ul>');
    $("#help_short_toc_content").append('<ul id="help_short_toc_list"></ul>');
    
    $("div.help_section").each(
      function(){
	var title = num.toString() + ". " +
	  $(this).children(".help_title").text();
        var li = "";
        var li_top = "";
        var subul = "";
        var link = "";
        var sublink = "";
        var subsublink = "";

        $(this).children(".help_title").text(title);
        subul = "<ul class=\"slide_ul\">";
        link = num.toString();

        $(this).attr({id: "help" + link});

        $(this).children(".help_subsection").each(
	  function(){
	    var subtitle =  num.toString() + "." + subnum.toString() +
	      ". " + $(this).children(".help_subtitle").html();

	    sublink = num.toString() + "_" + subnum.toString();
	    $(this).children(".help_subtitle").html(subtitle);
	    $(this).attr("id", "help" + sublink);

	    var subsubul = "<ul class=\"slide_ul\">";

	    $(this).children(".help_subsubsection").each(
	      function(){
		var subsubtitle = num.toString() + "." + subnum.toString() +
		  "."  + subsubnum.toString() + ". " +
		  $(this).children(".help_subsubtitle").text();
		subsublink = num.toString() + "_" + subnum.toString()+ "_" +
		  subsubnum.toString();
		$(this).children(".help_subsubtitle").text(subsubtitle);
		$(this).attr("id", "help" + subsublink);
		subsubul += "<li><a class=\"internal\" id=\"" + subsublink +
		  "\" href=\"#help" + subsublink + "\">" + subsubtitle +
		  "</a></li>";
		subsubnum = subsubnum + 1;
	      }
	    );

            subsubnum = 1;
            subsubul += "</ul>";

            if(subsubul == "<ul class=\"slide_ul\"></ul>"){
              subul += "<li><a class=\"internal\" id=\"" + sublink +
		"\" href=\"#help" + sublink + "\">" + subtitle + "</a></li>";
            }
            else{
              subul += "<span class=\"slide\"> + </span><li><a id=\"" +
		sublink+"\" class=\"slide internal\" href=\"#help" +
		sublink + "\">" + subtitle + "</a>";
            }
	    subul += subsubul + "</li>";
            subnum = subnum + 1;
	  }
	);

        subnum = 1;
        subul += "</ul>";
        if( subul == "<ul class=\"slide_ul\"></ul>"){
          li = "<li><a class=\"internal\" id=\"" + link +
	    "\" href=\"#help" + link + "\">" + title + "</a>";
        }
        else{
          li = "<span class=\"slide subul\"> + </span><li><a id=\"" +
	    link + "\" class=\"slide internal\" href=\"#help" + link + "\">" +
	    title + "</a>";
	}
        li += subul + "</li>";
        $(li).appendTo($("#help_toc_list"));

        li_top = "<li><a class=\"internal\" id=\"" + link +
	  "\" href=\"#help" + link + "\">" + title + "</a>";
        $(li_top).appendTo($("#help_short_toc_list"));

        num = num + 1;
      }
    );
  }

  $(window).load(
    function(){
      var target = location.hash && $(location.hash)[0];
      if (target){
	$.scrollTo(target, {speed:500});
      }
    }
  );

  // toc position change when window size change
  $(window).resize(
    function(){
      var winwidth = $(window).width();
      var containerwidth = $("#container").width();
      var diffwidth = (winwidth - containerwidth)/2 + 750;
      $("#help_tocs").fixedBox({x: diffwidth.toString(), y: "170"});
    }
  );

  $("#help_o").css("display", "none");
}