// ===== Ajoute et prepopulate les champs de subtasks quand on modifie ======
function create_fields_subtasks(subtask_list) {

   for(var i = 0 ; i < subtask_list.length ; i++){

      /*
      Ce qu'on crée à chaque fois, en HTML normal (peut-être qu'un .innerHTML aurait été judicieux) :

      <div class="input-group mb-2" id="test">
         <input type="text" name="new_subtask" class="form-control " placeholder="Nouvelle sous-tâche">
         <div class="input-group-append">
            <div class="input-group-text">
               <a href="JavaScript:Void(0);" onclick="remove_subtask('subN');" id="toggle_plus">
                  <i class="fa fa-times"></i>
               </a>
            </div>
         </div>
      </div>
      */

      var div_group = document.createElement("div");
      div_group.className = "input-group mb-2";
      div_group.id = "sub" + i;

      var input = document.createElement("input");
      input.type = "text";
      input.name = "new_subtask";
      input.id = "sub" + i + "field";
      input.value = subtask_list[i];
      input.className = "form-control";
      input.maxlength = "200";
      input.placeholder = "Nouvelle sous-tâche";

      var div_input_append = document.createElement("div");
      div_input_append.className = "input-group-append";

      var div_group_text = document.createElement("div");
      div_group_text.className = "input-group-text";

      var a_remove = document.createElement("a");
      a_remove.setAttribute("href", "javascript:void(0);");
      a_remove.setAttribute("onclick", "remove_subtask('sub" + i + "');");

      var times_i = document.createElement("i");
      times_i.className = "fa fa-times";

      a_remove.append(times_i);
      div_group_text.append(a_remove);
      div_input_append.append(div_group_text);
      div_group.append(input);
      div_group.append(div_input_append);

      document.getElementById("subtasks").prepend(div_group);
   }



}

// ===== Cache et enleve le subtask ======
function remove_subtask(id){
   var e = document.getElementById(id);
   e.style.display = 'none';
   var field_sub = document.getElementById(id + "field");
   field_sub.value = "";
}
