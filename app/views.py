from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UserForm
import json
from .models import User, Site, Campaign, Subscriber, Analytics
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, BrowsableAPIRenderer


def home(request):
    return render(request, "app/index.html", {"title": "Home Page"})


def index(request):
    if request.method == 'POST':
        uform = UserForm(request.POST)
        if uform.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # return HttpResponseRedirect('/thanks/')
            user = User(name=uform.cleaned_data['name'], email=uform.cleaned_data['email'], password=make_password(password=uform.cleaned_data['password'], salt=None, hasher="bcrypt"))
            user.save()
            site = Site(user=user, site_url="/")
            site.save()
            campaign = Campaign(site=site)
            campaign.save()
            return render(request, "app/signup.html", {"title": "Registered Successfully"})
        else:
            # return HttpResponse('POST method'+request.POST['name'])
            # request.session['name'] ="Session Created";
            print(request.session.get('name'))
            return render(request, "app/signup.html", {"title": "Registration Form Error"})
    else:  
        return render(request, "app/signup.html", {"title": "Registration Form"})


def client_dev_test(request):
    return render(request, "app/client_dev_test.html", {"title": "JavaScript Code Client Test", 'BASE_URL':request.get_host})


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
                return HttpResponseRedirect('/dashboard')
          else:
                return render(request, "app/login.html",{"title":"Login Form Failed"})
        except:
         return render(request, "app/login.html", {"title": "Login Form"})
    else:
         return render(request, "app/login.html", {"title": "Login Form"})


def dashboard(request):
     if "id" not in request.session:
         return HttpResponseRedirect('/signin')
     else:
        user = User.objects.get(id=request.session['id'])
        sites = Site.objects.filter(user=user)
        if request.session.get("site_id", None) is not None:
             site = Site.objects.get(id=request.session['site_id'])
        else:
            site = Site.objects.get(user=user, site_type="default")
            request.session['site_id'] = site.id
        campaigns = Campaign.objects.filter(site=site)  # getting campaigns of current site
        dashboardContext = {"title": "Welcome to Dashboard", "site": site, "sites": sites, "campaigns": campaigns}
        return render(request, "app/dashboard.html", dashboardContext)


def logout(request):
  request.session.flush()
  return HttpResponseRedirect('/')


@api_view(['POST'])
@renderer_classes((JSONRenderer, TemplateHTMLRenderer, BrowsableAPIRenderer))
def create_subscriber(request, format=None):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            site_token = request.POST['token']
            site = Site.objects.get(site_token=site_token)
            # need to get active campaign id from options instead of status
            campaign = Campaign.objects.get(id=1)
            campaign.subscriber_count += 1;
            percent = "{0:.2f}".format((campaign.subscriber_count * 100) / campaign.hits_count)
            campaign.conversion = percent
            campaign.save();
            subscriber = Subscriber(name=name, email=email, phone=phone, site=site, campaign=campaign)
            subscriber.save()
            data = '{"success":"true","message":"Record Created"}'
            return HttpResponse(data, content_type='application/json')
        except:
            print("Incorrect Data");
            return HttpResponse("Error occurred")


@api_view(['POST'])
@renderer_classes((JSONRenderer, TemplateHTMLRenderer, BrowsableAPIRenderer))
def notify(request, format=None):
    uuid = request.GET['quuid']
    ip = request.META['REMOTE_ADDR'];
    url = request.META['HTTP_REFERER']
    site_token = request.POST['token']
    unique_hits = 0
    try:
        analytic = Analytics.objects.get(cookie=uuid)
        unique_hits = 0
    except Analytics.DoesNotExist:
        analytics = Analytics(cookie=uuid, ip=ip, url=url, site_token=site_token)
        analytics.save()
        unique_hits = 1

    campaign = Campaign.objects.get(id=1)
    if campaign.hits_count == 0:
        percent = 0
    else:
        percent = "{0:.2f}".format((campaign.subscriber_count * 100) / campaign.hits_count)
    campaign.conversion = percent
    campaign.hits_count += 1;
    campaign.unique_hits +=unique_hits
    campaign.save();
    data = '{"success":"true","message":"Record Created"}'
    return HttpResponse(data, content_type='application/json')


@api_view(['POST'])
@renderer_classes((JSONRenderer, TemplateHTMLRenderer, BrowsableAPIRenderer))
def add_site(request, format=None):
    if request.method == 'POST':
        site_name = request.POST['site_name']
        if site_name != "":
            if "id" in request.session:
                user = User.objects.get(id=request.session['id'])
                site = Site(user=user,site_name=site_name, site_type="new", site_url="/")
                site.save()
                campaign = Campaign(site=site)
                campaign.save()
                return HttpResponse("ok")
            else:
                return HttpResponse("login first")
        else:
            return HttpResponse("Site name must not be blank")
    else:
        return HttpResponse(request.method+" Not supported")

@api_view(['POST'])
@renderer_classes((JSONRenderer, TemplateHTMLRenderer, BrowsableAPIRenderer))
def change_site(request, format=None):
    if request.method == 'POST':
        site_id = request.POST['site_id']
        request.session['site_id'] = site_id
        return HttpResponse("ok");
    else:
        return HttpResponse(request.method + " Not supported")
