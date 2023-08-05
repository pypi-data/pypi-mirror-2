# django imports
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

# lfc imports
from lfc.models import Portal

def load_data():

    site = Site.objects.all()[0]
    site.name = site.domain = "www.example.com"
    site.save()

    portal = Portal.objects.create()
    
    for i in range(1, 100):
        User.objects.create(username="User %s" % i)

def run():
    load_data()


