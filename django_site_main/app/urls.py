from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',

    url(r'^$', views.home, name='home'),
    url(r'^grades/$', views.grades, name='grades'),

)