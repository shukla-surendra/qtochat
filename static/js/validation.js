$("#loginForm").validate({
  rules: {
    password: "required",
    email: {
      required: true,
      email: true
    }
  },
  messages: {
    password: "Please provide your password",
    email: {
      required: "Please provide your email to login",
      email: "Your email address must be in the format of name@domain.com"
    }
  }
})


$("#signupForm").validate({
  rules: {
    password: "required",
    name: "required",
    url: "required",
    email: {
      required: true,
      email: true
    }
    
  },
  messages: {
    password: "Please enter your password",
    name: "Please Provide your name",
    url: "Please enter a valid website in the form: http://www.yourwebsite.com",
    email: {
      required: "Please provide your email to signup",
      email: "Your email address must be in the format of name@domain.com"
    } 

  }
})

