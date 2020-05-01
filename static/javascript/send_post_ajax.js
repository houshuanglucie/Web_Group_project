function post_form(url_endpoint){
   var members_chosen = [];
   const members = $(".place_member").children();

   for(var i = 0 ; i < members.length ; i++){
      var member = members[i];
      if(member.className.includes("member_box")){
      members_chosen.push(member.firstChild.data);
      }
   }

   var check_val = $("input[name='publicCheck']:checked").val()

   // console.log($("[name = csrfmiddlewaretoken]").val());
   // console.log(members_chosen);
   // console.log($("[name = name]").val())

   $.ajax({
      url : url_endpoint,
      type : "POST",
      data : {
         'csrfmiddlewaretoken' : $("[name = csrfmiddlewaretoken]").val(),
         'name' : $("[name = name]").val(),
         'members' : members_chosen,
         'publicCheck' : check_val,
      },

      success : function(json) {
         // console.log("SUCCESS");
         // console.log(json);
         $("#toast_body")[0].firstChild.data = json.name + " a été crée.";
         $('#toast_valid').toast('show');
      },

      error : function(json, err) {
         // console.log("FAILED");
         // console.log(err);
         $('#toast_member').toast('show');
      }
   });
}
