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

function load_parameters(build_line) {
  $("#parameters").empty();
    
  $.ajax({
    type: "GET",
    url: "/rest/build_lines/" + build_line + "/config/settings",
    dataType: "json",
    success: function(data){
      $("#parameters").append("<tr><th>Parameter</th><th>Value</th></tr>");
      for (var i=0; i<data.length; i++) {
        $("#parameters").append("<tr><td>"+data[i].name+"</td><td><input type='text' id='"+
                                data[i].name+"' value='"+data[i].value+"'/></td></tr>");
      }
    }
  });
}
$(document).ready(function(){

  $("#add_parameter").bind("click", function(){
    $("#add_form").css("display", "block");
  });
  
  var build_line = window.location.pathname.split("/")[2];
  
  $("#add_btn").bind("click", function(){
    $.ajax({
      type: "POST",
      url: "/rest/build_lines/" + build_line + "/config/settings",
      processData: false,
      data: '{"name": "' + $("#name").val() + '", "value": "' + $("#value").val() + '"}',
      contentType: "application/json",
      success: function(data){
        load_parameters(build_line);
      }
    });
    $("#add_form").css("display", "none");
  });
  
  load_parameters(build_line);
});
