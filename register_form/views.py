from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UserForm
from .models import User
from django.contrib.auth.hashers import make_password, check_password

def index(request):
    if request.method == 'POST':
       uform = UserForm(request.POST)
       if uform.is_valid():
           # process the data in form.cleaned_data as required
           # ...
           # redirect to a new URL:
           # return HttpResponseRedirect('/thanks/')
           user = User(name = uform.cleaned_data['name'], email = uform.cleaned_data['email'], password = make_password(password = uform.cleaned_data['password'], salt= None, hasher = "bcrypt"))
           user.save()
           return render(request, "form/form.html",{"title":"Registered Successfully"})
       else:
           #return HttpResponse('POST method'+request.POST['name'])
           #request.session['name'] ="Session Created";
           print(request.session.get('name'));
           return render(request, "form/form.html",{"title":"Registration Form Error"})
    else:  
       return render(request, "form/form.html",{"title":"Registration Form"})


def login(request):
     if request.method == 'POST':
        user_set = User.objects.filter(email=request.POST['email'])
        for user in user_set:
          email = user.email
          id = user.id
          name = user.name
          password = user.password
        try:
          email
          if check_password(request.POST['password'], password):
                request.session['id'] = id
                return HttpResponseRedirect('/form/dashboard')
          else:
                return render(request, "form/login.html",{"title":"Login Form Failed"})
        except:
         return render(request, "form/login.html",{"title":"Login Form"})
     else:
         return render(request, "form/login.html",{"title":"Login Form"})

def dashboard(request):
   if "id" not in request.session:
      return HttpResponseRedirect('/form/')
   else:
      user_set = User.objects.filter(id=request.session['id'])
      for user in user_set:
       name = user.name 
      return render(request, "form/dashboard.html",{"title":"Welcome to Dashboard", "name":name})

def logout(request):
  request.session.flush()
  return HttpResponseRedirect('/form/')
      



# Create your views here.
