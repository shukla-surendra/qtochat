
        
    url_signup = document.getElementById('url_signup');
    url = document.getElementById('url');
    url_signup.addEventListener("click", function(){
        modal_url = document.getElementById('modal_url')
        modal_url.value =  url.value
    })
    