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

function force_build(build_line) {
  $.ajax({
    type: "PUT",
    url: "/rest/build_lines/" + build_line,
    processData: false,
    data: '{"building": true}',
    contentType: "application/json",
    success: function(){
        $("#force_build").css('color', '#888');
        $("#force_build").unbind("click");
    }
  });
}
function pause_building(build_line) {
  $.ajax({
    type: "PUT",
    url: "/rest/build_lines/" + build_line,
    processData: false,
    data: '{"paused": true}',
    contentType: "application/json",
    success: function(){
        $("#paused").text('true');
        $("#pause").css('color', '#888');
        $("#pause").unbind('click');
        $("#resume").css('color', '#000');
        $("#resume").bind("click", function(){
            resume_building(build_line);
        });
        $("#force_build").css('color', '#888');
        $("#force_build").unbind("click");
    }
  });
}
function resume_building(build_line) {
  $.ajax({
    type: "PUT",
    url: "/rest/build_lines/" + build_line,
    processData: false,
    data: '{"paused": false}',
    contentType: "application/json",
    success: function(){
        $("#paused").text('false');
        $("#resume").css('color', '#888');
        $("#resume").unbind('click');
        $("#pause").css('color', '#000');
        $("#pause").bind("click", function(){
            pause_building(build_line);
        });
        $("#force_build").css('color', '#000');
        $("#force_build").bind("click", function() {
            force_build(build_line);
        });
    }
  });
}
function load_build_line(build_line) {
  $.ajax({
    type: "GET",
    url: "/rest/build_lines/" + build_line,
    dataType: "json",
    success: function(data){
        $("#name").text(data.name);
        $("#building").text(data.building);
        $("#paused").text(data.paused);
        $("#label").text(data.label);
        
        if (data.paused) {
            $("#pause").css('color', '#888');
            $("#force_build").css('color', '#888');
            $("#resume").bind("click", function(){
                resume_building(build_line);
            });
        } else {
            $("#resume").css('color', '#888');
            $("#pause").bind("click", function(){
                pause_building(build_line);
            });
            if (data.building) {
                $("#force_build").css('color', '#888');        
            } else {
                $("#force_build").bind("click", function(){
                    force_build(build_line);
                });
            }
        }
    }
  });
}
$(document).ready(function(){
  var build_line = window.location.pathname.split("/")[2];
  load_build_line(build_line);
});
