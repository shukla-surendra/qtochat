"""form_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.index, name="index"),
    path('signin', views.login, name="signin"),
    path('client_dev_test', views.client_dev_test, name="client_dev_test"),
    path('create_subscriber', views.create_subscriber , name="create_subscriber"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.logout, name="logout"),
    path('notify', views.notify, name="notify"),
    path('add_site', views.add_site, name="add_site"),
    path('change_site', views.change_site, name='change_site'),
    path('view_subscribers/<int:id>', views.view_subscribers, name='view_subscribers'),
    path('csv_export/<int:id>', views.csv_export, name='csv_export'),
]

# allow us to use '.json' and '.html' at the end of the url
#urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

