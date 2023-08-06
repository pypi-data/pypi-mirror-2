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

function load_machines_groups() {
  $("#machines_groups").empty();
    
  $.ajax({
    type: "GET",
    url: "/rest/machines_groups",
    dataType: "json",
    success: function(data){
      for (var i=0; i<data.length; i++) {
        $("#machines_groups").append("<tr><td><a href='/machines_groups/" + data[i].name + "'>" +
                                     data[i].name + "</a></td></tr>");
      }
    }
  });
}
$(document).ready(function(){

  $("#add_group").bind("click", function(){
    $("#add_form").css("display", "block");
  });
  
  $("#add_btn").bind("click", function(){
    $.ajax({
      type: "POST",
      url: "/rest/machines_groups",
      processData: false,
      data: '{"name": "' + $("#name").val() + '"}',
      contentType: "application/json",
      success: function(data){
        load_machines_groups();
      }
    });
    $("#add_form").css("display", "none");
  });
  
  load_machines_groups();
});
