// $('.datepicker').datepicker();


$(document).ready(function(){
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
                        console.log({data});
                    }, 
                    error: function(err){
                        console.log({err})
                    }
                })
              }



            }
        })




      
    })
  
})

