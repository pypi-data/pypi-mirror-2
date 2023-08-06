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

function load_machine(group, machine) {
  $.ajax({
    type: "GET",
    url: "/rest/machines_groups/"+group+"/machines/"+machine,
    dataType: "json",
    success: function(data){
        $("#info_name").text(data.name);
        $("#info_address").text(data.address);
        $("#info_port").text(data.port);
        $("#name").val(data.name);
        $("#address").val(data.address);
        $("#port").val(data.port);
    }
  });
}
$(document).ready(function(){

  $("#modify_machine").bind("click", function(){
    $("#modify_form").css("display", "block");
    $("#machine_info").css("display", "none");
  });
  
  var group = window.location.pathname.split("/")[2];
  var machine = window.location.pathname.split("/")[4];
  
  $("#save_btn").bind("click", function(){
    var name = $("#name").val();
    var address = $("#address").val()
    var port = $("#port").val()
    $.ajax({
      type: "PUT",
      url: "/rest/machines_groups/" + group + "/machines/" + machine,
      processData: false,
      data: '{"name": "'+name+'", "address": "'+address+'", "port": '+port+'}',
      contentType: "application/json",
      success: function(data){
        load_machine(group, machine);
        $("#modify_form").css("display", "none");
        $("#machine_info").css("display", "block");
      }
    });
  });
  
  load_machine(group, machine);
});
