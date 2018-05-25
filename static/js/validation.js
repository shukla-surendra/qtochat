$("#loginForm").validate({
  rules: {
    password: "required",
    email: {
      required: true,
      email: true
    }
  },
  messages: {
    password: "Please enter the password",
    email: {
      required: "Please provide your email to login",
      email: "Your email address must be in the format of name@domain.com"
    }
  }
})


$("#signupForm").validate({
  rules: {
    name: "required",
    password: "required",
    email: {
      required: true,
      email: true
    }
  },
  messages: {
    name: "Please Provide your name",
    password: "Please enter the password",
    email: {
      required: "Please provide your email to signup",
      email: "Your email address must be in the format of name@domain.com"
    }
  }
})