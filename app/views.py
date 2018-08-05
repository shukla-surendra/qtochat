from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import UserForm, widgetCustomizationForm
from .models import widget_customization
import json
import csv
import uuid
import os
from .models import User, Site, Campaign, Subscriber, Analytics
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, BrowsableAPIRenderer

##Email modules
from django.template.loader import get_template
import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def home(request):
    return render(request, "app/index.html", {"title": "Home Page"})


def signup(request):
    serverRes = {}
    if request.method == 'POST':

        user_token = uuid.uuid4()
        UserExist = User.objects.filter(email=request.POST['email'])
        if not UserExist:

            user = User(name=request.POST['name'], 
            email=request.POST['email'], 
            password=make_password(request.POST['password'], 
            salt=None, hasher="bcrypt"),
            user_token=user_token)
            user.save()

            if not user:
                print("Registration failed.")
            else:
                site = Site(user=user, site_url="/")
                site.save()
                campaign = Campaign(site=site)
                campaign.save()
                
                # Replace sender@example.com with your "From" address. 
                # This address must be verified.
                SENDER = 'support@qtochat.com'  
                SENDERNAME = 'Qtochat'

                # Replace recipient@example.com with a "To" address. If your account 
                # is still in the sandbox, this address must be verified.
                RECIPIENT  = request.POST['email']

                # Replace smtp_username with your Amazon SES SMTP user name.
                USERNAME_SMTP = "YOUR_SES_SMTP_USERNAME"

                # Replace smtp_password with your Amazon SES SMTP password.
                PASSWORD_SMTP = "YOUR_SES_SMTP_PASSWORD"

                # (Optional) the name of a configuration set to use for this message.
                # If you comment out this line, you also need to remove or comment out
                # the "X-SES-CONFIGURATION-SET:" header below.
                #CONFIGURATION_SET = "ConfigSet"

                # If you're using Amazon SES in an AWS Region other than US West (Oregon), 
                # replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP  
                # endpoint in the appropriate region.
                HOST = "email-smtp.us-east-1.amazonaws.com"
                PORT = 587

                # The subject line of the email.
                SUBJECT = 'Welcome to the Qtochat Family'

                # The email body for recipients with non-HTML email clients.
                BODY_TEXT = (" Thank you for registering on Qtochat, to complete your registration, please visit this URL: https://qtochat.com/token")

                # The HTML body of the email.
                userTitle = User.objects.get(email=request.POST['email'])
                context = {
                        'title': userTitle.name,
                        'token': userTitle.user_token
                }
                htmlT = get_template('app/welcome_email.html').render(context)
                BODY_HTML = htmlT
                # Create message container - the correct MIME type is multipart/alternative.
                msg = MIMEMultipart('alternative')
                msg['Subject'] = SUBJECT
                msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
                msg['To'] = RECIPIENT
                
                # Comment or delete the next line if you are not using a configuration set
                #msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

                # Record the MIME types of both parts - text/plain and text/html.
                part1 = MIMEText(BODY_TEXT, 'plain')
                part2 = MIMEText(BODY_HTML, 'html')

                # Attach parts into message container.
                # According to RFC 2046, the last part of a multipart message, in this case
                # the HTML message, is best and preferred.
                msg.attach(part1)
                msg.attach(part2)

                # Try to send the message.
                try:  
                    server = smtplib.SMTP(HOST, PORT)
                    server.ehlo()
                    server.starttls()
                    #stmplib docs recommend calling ehlo() before & after starttls()
                    server.ehlo()
                    server.login(USERNAME_SMTP, PASSWORD_SMTP)
                    server.sendmail(SENDER, RECIPIENT, msg.as_string())
                    server.close()
                # Display an error message if something goes wrong.
                except Exception as e:
                    print ("Error: ", e)
                else:
                    print ("Email sent!")
                return render(request, "app/verify.html", {"title": "Registered Successfully"})
        else:
            serverRes = {
                "response": "A user with this login credentials has already been registered, please login to continue"
            }

    return render(request, "app/createaccount.html", serverRes)

def verify(request):
        return render(request, 'app/verify.html')

def client_dev_test(request):
        return render(request, "app/client_dev_test.html", {"title": "JavaScript Code Client Test", 'BASE_URL':request.get_host})


def signin(request):
    ''' User authentication function for login '''
    if "id" in request.session:
            return HttpResponseRedirect('/myadmin')
    else:

        #check if form has been submitted
        if request.method == 'POST':
            user_set = User.objects.filter(email=request.POST['email'])
            #check if user-entered information matches the information in the database
            if not user_set:
                return render(request, "app/login.html", {"result": "You entered an invalid username and password"})
            else:
                for user in user_set:
                    email = user.email
                    id = user.id
                    password = user.password
                    if check_password(request.POST['password'], password) and request.POST['email']==email:
                        request.session['id'] = id

                        # if request.POST['remember_me']:
                        #     request.session.set_expiry(0)
                        #     print(request.session.get_expiry_age())

                        return HttpResponseRedirect('/myadmin')
                    else:
                        return render(request, "app/login.html", {"title": "Login Form Failed"})
        else:
                return render(request, "app/login.html", {"title": "Login Form"})

def activate(request, token):

    urlToken = User.objects.filter(user_token=token)
    if not urlToken:
        context = {
            'result': "Sorry, you don't have an accouint with us, please, register. Thank you"
        }
        return render(request, 'app/activate.html', context)
    if urlToken:
        for urlpart in urlToken:
            if urlpart.user_token==token and urlpart.status=='0':
                urlpart.user_status="1"
                urlpart.save()

                context = {
                    "result": "Your account has been activated"
                }
                return render(request, 'app/activate.html', context)
            else:
                context = {
                    "result": "Your account has been activated already, please log in"
                }
                return render(request, 'app/activate.html', context) 
        
    return render(request, 'app/activate.html')

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
            percent = "{0:.2f}".format((campaign.subscriber_count * 100) / campaign.unique_hits)
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
        percent = "{0:.2f}".format((campaign.subscriber_count * 100) / campaign.unique_hits)
    campaign.conversion = percent
    campaign.hits_count += 1;
    campaign.unique_hits += unique_hits
    campaign.save();
    question_set = '[{"question": "Hey Provide your email Address", "answer_type": "input", "validation_type": "email"}, { "question": "Hey Provide your Name", "answer_type": "input", "validation_type": "name"}]'
    data = '{"success":"true", "message": "Record Created", "question": '+question_set+'}'
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
        return HttpResponse("ok")
    else:
        return HttpResponse(request.method + " Not supported")


def view_subscribers(request, id=0):
    campaign = Campaign.objects.get(id=id);
    subscriber_list = Subscriber.objects.filter(campaign=campaign)
    paginator = Paginator(subscriber_list, 10)  # Show 25 contacts per page

    page = request.GET.get('page', 1)
    subscriber = paginator.get_page(page)
    subscriber_context = {"subscribers": subscriber, "campaign_id": id}
    return render(request, "app/view_subscribers.html", subscriber_context)


def csv_export(request, id=0):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone'])
    campaign = Campaign.objects.get(id=id)
    subscriber_list = Subscriber.objects.filter(campaign=campaign)
    for subscriber in subscriber_list:
        writer.writerow([subscriber.name, subscriber.email, subscriber.phone])
    return response

def myadmin(request):
    

    title= "Qtochat Admin Panel"

    context = {
        "title":title
    }

    return render(request, "app/myadmin.html", context)

def Widget_customization(request):
    if request.method == 'POST':
        #from model.py
        
        customize = widget_customization.objects.get(id=2)
        customize.widget_color = "#999"
        customize.save(['#999'])

        #insert into the database
        # add this when you install bcrypt: username = request.session['id'], sitename = request.session['site_id']
        # customization = widget_customization(widget_color=request.POST['textcolor'], widget_background=request.POST['base-color'], widget_outer_ring_color=request.POST['outer-ring'])
        # customization.save()

        # print(uform.widget_background)
        return redirect('myadmin')

def login(request):

    return render(request, "app/login.html")

def createaccount(request):
    return render(request, "app/createaccount.html")

def recover(request):

    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if not user:
            context = {
                "result": "You are not registered with us with this email address, please enter your Qtochat email address"
            }
            return render(request, "app/recover.html", context)
        else:
            # Replace sender@example.com with your "From" address. 
                    # This address must be verified.
                    SENDER = 'support@qtochat.com'  
                    SENDERNAME = 'Qtochat'

                    # Replace recipient@example.com with a "To" address. If your account 
                    # is still in the sandbox, this address must be verified.
                    RECIPIENT  = request.POST['email']

                    # Replace smtp_username with your Amazon SES SMTP user name.
                    USERNAME_SMTP = "YOUR_SES_SMTP_USERNAME"

                    # Replace smtp_password with your Amazon SES SMTP password.
                    PASSWORD_SMTP = "YOUR_SES_SMTP_PASSWORD"

                    # (Optional) the name of a configuration set to use for this message.
                    # If you comment out this line, you also need to remove or comment out
                    # the "X-SES-CONFIGURATION-SET:" header below.
                    #CONFIGURATION_SET = "ConfigSet"

                    # If you're using Amazon SES in an AWS Region other than US West (Oregon), 
                    # replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP  
                    # endpoint in the appropriate region.
                    HOST = "email-smtp.us-east-1.amazonaws.com"
                    PORT = 587

                    # The subject line of the email.
                    SUBJECT = 'Password reset'
                    newpassword = str(os.urandom(8))
                    # The email body for recipients with non-HTML email clients.
                    BODY_TEXT = (" Your new password is: "+ newpassword + "please, change your password as soon as possible")

                    # The HTML body of the email.
                    userTitle = User.objects.get(email=request.POST['email'])
                    context = {
                            'title': userTitle.name,
                            'token': userTitle.user_token,
                            'newpassword':newpassword
                    }
                    userTitle.password=make_password(newpassword, salt=None, hasher="bcrypt")
                    userTitle.save()
                    
                    htmlT = get_template('app/reset.html').render(context)
                    BODY_HTML = htmlT
                    # Create message container - the correct MIME type is multipart/alternative.
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = SUBJECT
                    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
                    msg['To'] = RECIPIENT
                    
                    # Comment or delete the next line if you are not using a configuration set
                    #msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

                    # Record the MIME types of both parts - text/plain and text/html.
                    part1 = MIMEText(BODY_TEXT, 'plain')
                    part2 = MIMEText(BODY_HTML, 'html')

                    # Attach parts into message container.
                    # According to RFC 2046, the last part of a multipart message, in this case
                    # the HTML message, is best and preferred.
                    msg.attach(part1)
                    msg.attach(part2)

                    # Try to send the message.
                    try:  
                        server = smtplib.SMTP(HOST, PORT)
                        server.ehlo()
                        server.starttls()
                        #stmplib docs recommend calling ehlo() before & after starttls()
                        server.ehlo()
                        server.login(USERNAME_SMTP, PASSWORD_SMTP)
                        server.sendmail(SENDER, RECIPIENT, msg.as_string())
                        server.close()
                    # Display an error message if something goes wrong.
                    except Exception as e:
                        print ("Error: ", e)
                    else:
                        print ("Email sent!")
                        return render(request, "app/recover.html", {"result":"Please, check your email for your new password"})
    return render(request, "app/recover.html")

