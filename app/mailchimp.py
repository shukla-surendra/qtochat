from mailchimp3 import MailChimp
from .models import User, Mailchimp
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from .models import User, Site, Subscriber
import datetime

import json


def integrate(request, APIkey, listId):
    #quey the database to check if user has their mailchimo integated
    ''' if user is integrated then show user data else show integrate button'''
    #Ping Mailchimp to be sure the apikey and list ID returns a value
    if pingIntegration(request, APIkey, listId) == True:
        id = request.session['id']
        user = User.objects.get(id=id)
        addIntegration = Mailchimp(user=user, apikey=APIkey, listId=listId)
        addIntegration.save()
    else:
        return HttpResponse("Please Enter A Valid API Key And List ID")


def showList(request):
    ''' This will show the members in a list that has been collected by your chatbot from all your sites '''
    #getSites
    user = User.objects.get(id=request.session['id'])
    sitename = request.POST['sitename']
    sites = Site.objects.filter(user=user, site_name=sitename)

    for site in sites:
        # getsubscribers based on the sites
        subscribers = Subscriber.objects.filter(
            site=site
            # created_at__gte=datetime.date(2018, 8, 29),
            # created_at__lte=datetime.date(2018, 8, 30)
        )
        # print(subscribers)
        newsubscribers = {}

        for subscriber in subscribers:
            newsubscribers[subscriber.name] = [subscriber.email]

        return HttpResponse(str(newsubscribers))


#ping the api
def pingIntegration(request, APIkey, listId):
    client = MailChimp(APIkey)
    client = client.lists.members.all(
        listId, count=1, offset=0, fields="members.email_address")
    if not client:
        return False
    else:
        return True
