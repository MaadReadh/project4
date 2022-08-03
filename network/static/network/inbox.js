// document.addEventListener('DOMContentLoaded',function(){
//     btn_list=document.querySelectorAll('button');
//     btn_list.forEach(editPost);
//     edit_list=document.querySelectorAll('a');
//     edit_list.forEach(showLike);


    function like(button, postId) {
      toggle_like_ui(button);
      button.disabled = true;
      fetch("/like", {
        method: "post",
        body: JSON.stringify({
          id: postId,
        }),
      })
        .then((res) => {
          if (res.status != 200) {
            toggle_like_ui(button);
          }
          button.disabled = false;
        })
        .catch((e) => {
          console.log(e)
          button.disabled = false;
        });
    }
    
    function toggle_like_ui(button) {
      iconEl = button.querySelector(".fa-heart");
      countEl = button.querySelector(".likes_count");
      if (button.querySelector(".fa-heart").classList.contains("fa-solid")) {
        countEl.innerHTML = `${parseInt(countEl.innerHTML) - 1}`;
        iconEl.classList.remove("fa-solid", "text-danger");
      } else {
        countEl.innerHTML = `${parseInt(countEl.innerHTML) + 1}`;
        iconEl.classList.add("fa-solid", "text-danger");
      }
    }
//  function editPost(item){
    
//            item.addEventListener('click', function(){
//            console.log(item.dataset.id);
//            if (item.dataset.id === undefined){}
//            else{
    
//            post_id=item.dataset.id;
    
//            post_body=document.getElementById(post_id+'div');
//            post_body.style.visibility = "hidden";
//            post_txt=document.getElementById(post_id+'p');
//            post_date=document.getElementById(post_id+'d');
//            edit_form=document.getElementById(post_id+'form');
//            edit_form.style.display ='block';
//            edit_post_body=document.getElementById(post_id+'textarea');
    
//             edit_form.onsubmit= function(){
//             let new_post=edit_post_body.value
//            console.log("from js "+new_post);


//            fetch(`/EditPost/${post_id}`, {
//                method: 'POST',
//                body: JSON.stringify({
//                    body: edit_post_body.value
//                })
//              })
//              .then(response => response.json())
//              .then(result => {
                 
//                  console.log(result);
//                  if (result.message != null)
//                  {  console.log("correct");
    
//            edit_form.style.display ='none';
//            post_body.style.visibility = "visible";
    
//                  }
//                    if (result.error != null)
//                  {  console.log("incorrect");}
//              });
    
//            return false;
//                }
    
//            }
    
//            })
    
//            }
// })