// ===== Se charge du drag and drop des membres ======
function initiate_drag(){
   const draggables = document.querySelectorAll('.member_box');
   const place_user = document.querySelectorAll('.place_user')[0];
   const place_member = document.querySelectorAll('.place_member')[0];

   let draggedItem = null;


   for (let i = 0; i < draggables.length; i++) {
      const item = draggables[i];

      item.addEventListener('dragstart', function () {
         draggedItem = item;
         setTimeout(function () {
            item.style.display = 'none';
         }, 0)
      });

      item.addEventListener('dragend', function () {
         setTimeout(function () {
            draggedItem.style.display = 'block';
            draggedItem = null;
         }, 0);
      })



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
         this.append(draggedItem);
         this.style.backgroundColor = 'rgba(0, 0, 0, 0)';
      });




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
         this.append(draggedItem);
         this.style.backgroundColor = 'rgba(0, 0, 0, 0)';
      });


   }
}




// ===== Fait une requete POST ======
