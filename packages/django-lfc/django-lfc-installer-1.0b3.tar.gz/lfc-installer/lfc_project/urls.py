# python imports
import os

# django imports
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic.simple import direct_to_template

admin.autodiscover()
DIRNAME = os.path.dirname(__file__)

# handler500 = 'lfc.views.server_error'

# Django 
urlpatterns = patterns('',
    url('^accounts/login/?$', login, {"template_name" : "admin/login.html"}, name='auth_login'),
    url('^accounts/logout/?$', logout, name='auth_logout'),

    (r'^admin/(.*)', admin.site.root),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(DIRNAME, "media"), 'show_indexes': True }),
)

# Contact Form
urlpatterns += patterns('contact_form.views',
   url(r'^contact$', "contact_form", { 'success_url': 'contact-thank-you' }, name='contact_form'),
   url(r'^contact-thank-you$', direct_to_template, { 'template': 'contact_form/contact_form_sent.html' }, name='contact_form_sent'),
)

# LFC Blog
urlpatterns += patterns("",
    (r'', include('lfc_blog.urls')),
)

# LFC
urlpatterns += patterns('',
    (r'^manage/', include('lfc.manage.urls')),
    (r'', include('lfc.urls')),
)