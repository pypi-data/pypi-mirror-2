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
 * Tooltip script 
 * powered by jQuery (http://www.jquery.com)
 * 
 * written by Alen Grakalic (http://cssglobe.com)
 * 
 * for more info visit http://cssglobe.com/post/1695/easiest-tooltip-and-image-preview-using-jquery
 *
 */
(function($){

	$.fn.tooltip = function(settings){	

		settings = jQuery.extend({
			xOffset			: 10,
			yOffset			: 20,
			display_class	: "tooltip"
		}, settings);

		if ($(this).attr("title") != "") { 
		
			$(this).hover(function(e){										  
				this.t = this.title;
				this.title = "";									  
				$("body").append("<p class='" + settings["display_class"] + "'>"+ this.t +"</p>");
				$("."+settings["display_class"])
					.css("top",(e.pageY - settings["xOffset"]) + "px")
					.css("left",(e.pageX + settings["yOffset"]) + "px")
					.fadeIn("fast");		
		    },
			function(){
				this.title = this.t;		
				$("."+settings["display_class"]).remove();
		    });	
			$(this).mousemove(function(e){
				$("."+settings["display_class"])
					.css("top",(e.pageY - settings["xOffset"]) + "px")
					.css("left",(e.pageX + settings["yOffset"]) + "px");
			});			
		}
	};

})(jQuery)
