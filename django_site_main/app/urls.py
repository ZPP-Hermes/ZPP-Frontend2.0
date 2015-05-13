from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',

    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^grades/$', views.grades, name='grades'),
    url(r'^oauth_callback/$', views.oauth_callback, name='oauth'),
    url(r'^oauth_init/$', views.oauth_init, name='oauth'),

)