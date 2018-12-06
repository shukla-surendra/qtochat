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

  if (url.value === "") {
    document.getElementById("uresponse").innerHTML = "Field can't be empty";
  }

  if (name.value === "") {
    document.getElementById("nresponse").innerHTML = "Field can't be empty";
  }
  if (email.value === "") {
    document.getElementById("eresponse").innerHTML = "Field can't be empty";
  }
  if (password.value === "") {
    document.getElementById("presponse").innerHTML = "Field can't be empty";
  }
  if (password2.value === "") {
    document.getElementById("presponse").innerHTML = "Field can't be empty";
  }

  if (password.value !== password2.value) {
    document.getElementById("presponse").innerHTML =
      "Your first password and second password must match";
  }

  $.ajax({
    type: "POST",
    url: "signup",
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
      //obj = JSON.parse(response);
      hello = document.getElementById("#progress");
      window.location = "verify";
    },

    error: function(xhr, status, error) {
      alert("failed" + error);
    }
  });
  e.preventDefault();
});
