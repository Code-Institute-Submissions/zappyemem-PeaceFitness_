

$(document).ready(function(){

    $('.datepicker').datepicker();
    
    $('.delete_training').on('click', function(e){
        e.preventDefault();
        let item_id = $(this).attr('id'); 
        console.log({item_id}); 

        bootbox.confirm({
            size: "small",
            message: "Are you sure you want to delete this ?",
            callback: function (result) { /* result is a boolean; true = OK, false = Cancel*/
              if(result==true){
                  
                $.ajax({
                    methof: "GET", 
                    url: `/delete_training/${item_id}`, 
                    cache: false, 
                    success:function(data){
                        window.location.reload(); 
                    }, 
                    error: function(err){
                        window.location.reload(); 

                    }
                })
              }



            }
        })




      
    })


    $('.delete_category').on('click', function(e){
        e.preventDefault();
        let item_id = $(this).attr('id'); 
      

        bootbox.confirm({
            size: "small",
            message: "Are you sure you want to delete this category?",
            callback: function (result) { /* result is a boolean; true = OK, false = Cancel*/
              if(result==true){
                  
                $.ajax({
                    methof: "GET", 
                    url: `/delete_category/${item_id}`, 
                    cache: false, 
                    success:function(data){
                        window.location.reload(); 
                    }, 
                    error: function(err){
                        window.location.reload(); 

                    }
                })
              }



            }
        })




      
    })

    $('.logout_btn').on('click', function(e){
        e.preventDefault(); 

        bootbox.confirm({
            size: "small",
            message: "Are you sure you want to logout ?",
            callback: function (result) { /* result is a boolean; true = OK, false = Cancel*/
              if(result==true){
                  window.location.href="/logout"
               
              }



            }
        })
    })
  
})

