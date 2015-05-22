from django.conf.urls import patterns, url, include

from app import views

urlpatterns = patterns('',

                       url(r'^$', views.home, name='home'),
                       url('^', include('django.contrib.auth.urls')),
                       url(r'^edit_marks/', views.edit_marks, name='edit_marks'),
                       url(r'^commit_edit/(\d+)', views.mark_edit, name='commit_edit'),
                       url(r'^grades/$', views.grades, name='grades'),
                       url(r'^gradesDynamic/$', views.gradesDynamic, name='gradesDynamic'),
                       url(r'^gradesDynamic/filter$', views.gradesFilter, name='gradesFilter'),
                       url(r'^oauth_callback/$', views.oauth_callback, name='oauth'),
                       url(r'^oauth_init/$', views.oauth_init, name='oauth'),

)