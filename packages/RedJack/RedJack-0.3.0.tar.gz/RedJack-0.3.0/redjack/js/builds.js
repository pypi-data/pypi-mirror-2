// Copyright (C) 2010-2011 Michal Nowikowski <godfryd@gmail.com>
// All rights reserved.
//
// Permission  is  hereby granted,  free  of charge,  to  any person
// obtaining a  copy of  this software  and associated documentation
// files  (the  "Software"),  to   deal  in  the  Software   without
// restriction,  including  without limitation  the  rights to  use,
// copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies  of  the  Software,  and to  permit  persons  to  whom the
// Software  is  furnished  to  do  so,  subject  to  the  following
// conditions:
//
// The above copyright  notice and this  permission notice shall  be
// included in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS  IS", WITHOUT WARRANTY OF ANY  KIND,
// EXPRESS OR IMPLIED, INCLUDING  BUT NOT LIMITED TO  THE WARRANTIES
// OF  MERCHANTABILITY,  FITNESS   FOR  A  PARTICULAR   PURPOSE  AND
// NONINFRINGEMENT.  IN  NO  EVENT SHALL  THE  AUTHORS  OR COPYRIGHT
// HOLDERS  BE LIABLE  FOR ANY  CLAIM, DAMAGES  OR OTHER  LIABILITY,
// WHETHER  IN AN  ACTION OF  CONTRACT, TORT  OR OTHERWISE,  ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
// OTHER DEALINGS IN THE SOFTWARE.

function load_builds(build_line) {
    $("#builds").empty();
    
    $.ajax({
	type: "GET",
	url: "/rest/build_lines/" + build_line + "/builds",
	dataType: "json",
	success: function(data){
	    $("#builds").append("<tr><th>Builds</th><th>Version</th><th>State</th><th>Start</th><th>End</th></tr>");
	    for (var i=0; i<data.length; i++) {
		var b = data[i];
		var row = "<tr><td><a href='/build_lines/" + build_line + "/builds/" + b.label + "'>";
		row += b.label + "</a></td>";
		row += "<td>" + b.version + "</td>";
		row += "<td>" + b.state + "</td>";
		row += "<td>" + b.start_date + "</td>";
		row += "<td>" + b.end_date + "</td>";
		row += "</tr>";
		$("#builds").append(row);
	    }
	}
    });
}
$(document).ready(function(){
    var build_line = window.location.pathname.split("/")[2];
    load_builds(build_line);
});
