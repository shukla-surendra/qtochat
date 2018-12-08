$(".carousel").carousel();

// capture user details on registration from home page
url = document.getElementById("url");
modal_url = document.getElementById("modal_url");

signup_link = document.getElementById("signup_link");
signup_link.addEventListener("click", function() {
  modal_url.value = url.value;
});

// frontend signup

$(document).on("submit", "#register", function(e) {
  e.preventDefault();
  let password = document.getElementById("password");
  let password2 = document.getElementById("password2");
  let url = document.getElementById("modal_url");
  let name = document.getElementById("name");
  let email = document.getElementById("email");
  var loading = document.getElementById("loading");
  loading.style.display = "block";

  if (url.value === "") {
    document.getElementById("uresponse").innerHTML = "Field can't be empty";
    loading.style.display = "none";
  }

  if (name.value === "") {
    document.getElementById("nresponse").innerHTML = "Field can't be empty";
    loading.style.display = "none";
  }
  if (email.value === "") {
    document.getElementById("eresponse").innerHTML = "Field can't be empty";
    loading.style.display = "none";
  }
  if (password.value === "") {
    document.getElementById("presponse").innerHTML = "Field can't be empty";
    loading.style.display = "none";
  }
  if (password2.value === "") {
    document.getElementById("presponse").innerHTML = "Field can't be empty";
  }

  if (password.value !== password2.value) {
    document.getElementById("presponse").innerHTML =
      "Your first password and second password must match";
    loading.style.display = "none";
  }

  setTimeout(register, 1000);
  //start of ajax request

  function register() {
    loading.style.display = "none";
    $.ajax({
      type: "POST",
      url: "xhr_signup",
      //dataType: "json",
      data: {
        url: $("#modal_url").val(),
        name: $("#name").val(),
        email: $("#email").val(),
        password: $("#password").val(),
        password2: $("#password2").val(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
      },

      success: function(response) {
        //alert(response);
        // obj = JSON.parse(response);
        console.log(response);
        if (response === "Registered Successfully") {
          window.location = "verify";
        }
        // if (response === "No field should be empty") {
        //   loading.style.display = "none";
        //   document.getElementById("progressinfo").innerHTML =
        //     "No field should be empty";
        // }
        if (response === "Registration failed") {
          loading.style.display = "block";
          document.getElementById("progressinfo").innerHTML =
            "Registration failed";
        }

        if (response === "userexist") {
          document.getElementById("progressinfo").innerHTML =
            "A user with this email exist. Please, use a different email address";
        }
      },

      error: function(xhr, status, error) {
        alert("failed" + error + status);
      }
    });
  }
  //end of ajax
  e.preventDefault();
});
