"""
Definition of urls for django_site_main.
"""

from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.contrib import admin
import os
admin.autodiscover()

import settings
urlpatterns = patterns('',
                       url(r'^', include('app.urls', namespace='app')),

                       # url(r'^login/$',
                       # 'django.contrib.auth.views.login',
                       # {
                       #         'template_name': 'app/login.html',
                       #         'authentication_form': BootstrapAuthenticationForm,
                       #         'extra_context':
                       #         {
                       #             'title':'Log in',
                       #             'year':datetime.now().year,
                       #         }
                       #     },
                       #     name='login'),
                       # url(r'^logout$',
                       #     'django.contrib.auth.views.logout',
                       #     {
                       #         'next_page': '/',
                       #     },
                       #     name='logout'),

                       # url(r'^$', 'app.views.home', name='home'),
                       # url(r'^contact$', 'app.views.contact', name='contact'),
                       # url(r'^about', 'app.views.about', name='about'),
                       # url(r'^oauth_callback', 'app.views.oauth_callback', name='oauth'),
                       # url(r'^oauth_init', 'app.views.oauth_init', name='oauth'),
                       # url(r'^login/$',
                       #     'django.contrib.auth.views.login',
                       #     {
                       #         'template_name': 'app/login.html',
                       #         'authentication_form': BootstrapAuthenticationForm,
                       #         'extra_context':
                       #         {
                       #             'title':'Log in',
                       #             'year':datetime.now().year,
                       #         }
                       #     },
                       #     name='login'),
                       # url(r'^logout$',
                       #     'django.contrib.auth.views.logout',
                       #     {
                       #         'next_page': '/',
                       #     },
                       #     name='logout'),
                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
