$("#site_view").on("change", function(){

site_id = $(this).val();

$.ajax({
     type:'POST',
     data:'site_id='+site_id,
     url:'/change_site',
     success:function(res, status, xhr)
     {
         if(res == "ok")
         {
             location.reload();
         }

     }
})

})


function openCity(evt, cityName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}

$(".tab .first").trigger("click");

function site_save_changes()
{
   data = "site_name="+$("#site_name").val();
   $.ajax({
   url:'/add_site',
   type:'post',
   data:data,
   success: function(result, status, xhr){
        if(result == "ok")
        {
         $("#msg_danger").hide();
        $("#msg_success").show();
        setInterval(function(){
        location.reload();
        },200)

        }
        else
        {
        $("#msg_danger").text(result);
        $("#msg_danger").show();
        }
   }
   })
}