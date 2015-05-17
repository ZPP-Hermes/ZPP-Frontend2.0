from django.conf.urls import patterns, url, include

from app import views

urlpatterns = patterns('',

    url(r'^$', views.home, name='home'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^grades/$', views.grades, name='grades'),

)