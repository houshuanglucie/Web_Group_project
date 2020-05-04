// ===== Se charge du drag and drop des membres ======
function initiate_drag(){
   const draggables = document.querySelectorAll('.member_box');
   const place_user = document.querySelectorAll('.place_user')[0];
   const place_member = document.querySelectorAll('.place_member')[0];

   let draggedItem = null;


   for (let i = 0; i < draggables.length; i++) {
      const item = draggables[i];

      // Si on detecte un drag, on va se focaliser sur cet item
      // et on arrete de l'afficher dans son endroit d'origine
      item.addEventListener('dragstart', function () {
         draggedItem = item;
         setTimeout(function () {
            item.style.display = 'none';
         }, 0)
      });

      // Si on  l'a lache, c'est bon, on peut le ré-afficher et arreter de se focus dessus
      item.addEventListener('dragend', function () {
         setTimeout(function () {
            draggedItem.style.display = 'block';
            draggedItem = null;
         }, 0);
      })


      // Si on passe sur le champ des users non membres, on mets le fond en rouge, et quelques autres trucs
      place_user.addEventListener('dragover', function (e) {
         e.preventDefault();
         this.style.backgroundColor = 'rgba(255, 0, 0, 0.1)';
      });

      place_user.addEventListener('dragenter', function (e) {
         e.preventDefault();
         this.style.backgroundColor = 'rgba(255, 0, 0, 0.1)';
      });

      place_user.addEventListener('dragleave', function (e) {
         this.style.backgroundColor = 'rgba(0, 0, 0, 0)';
      });

      place_user.addEventListener('drop', function (e) {
         this.append(draggedItem); // On ajoute a sa progeniture ce qu'on vient de drag
         this.style.backgroundColor = 'rgba(0, 0, 0, 0)';
      });



      // Si on passe sur le champ des users membres du projet, on mets le fond en vert, et quelques autres trucs
      place_member.addEventListener('dragover', function (e) {
         e.preventDefault();
         this.style.backgroundColor = 'rgba(0, 255, 0, 0.1)';
      });

      place_member.addEventListener('dragenter', function (e) {
         e.preventDefault();
         this.style.backgroundColor = 'rgba(0, 255, 0, 0.1)';
      });

      place_member.addEventListener('dragleave', function (e) {
         this.style.backgroundColor = 'rgba(0, 0, 0, 0)';
      });

      place_member.addEventListener('drop', function (e) {
         this.append(draggedItem); // On ajoute a sa progeniture ce qu'on vient de drag
         this.style.backgroundColor = 'rgba(0, 0, 0, 0)';
      });


   }
}
