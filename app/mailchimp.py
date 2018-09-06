from mailchimp3 import MailChimp
from .models import User, Mailchimp
from django.conf import settings


def integrate(request, APIkey, listId):
        #quey the database to check if user has their mailchimo integated
        ''' if user is integrated then show user data else show integrate button'''
        id = request.session['id']
        user = User.objects.get(id=id)
        addIntegration= Mailchimp(user=user,apikey=APIkey, listId=listId)
        addIntegration.save()
def showList():
        ''' This will show the members in a list that has been collected by your chatbot '''
        pass        