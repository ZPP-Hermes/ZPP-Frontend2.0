# coding=utf-8
"""
Definition of views.
"""
from datetime import datetime
import urlparse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
import urlparse
import oauth2 as oauth
import requests
import numpy as np
import json

from forms import *
from models import *
import Predictions

consumer = oauth.Consumer(key='uvTtX63RWFaCf9pAxdtT', secret='5Jn3t9KNVMvSCeBtREX3nCvcKAnL55UrJKbcTvxD')


def register(request):
    if request.user.is_authenticated():
        return redirect('app:home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})


def home(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/index.html',
        context_instance=RequestContext(request,
                                        {
                                            'title': 'Strona domowa',
                                            'year': datetime.now().year,
                                        })
    )


@login_required()
def edit_marks(request):
    courses = Course.objects.all()
    lst = []
    for course in courses:
        i_id = course.pk
        try:
            instance = SavedMark.objects.get(course__pk=i_id, user=request.user)
        except SavedMark.DoesNotExist:
            lst.append({"name": course.name, "i_id": i_id, "form": SavedMarkForm(), "mode": False})
            continue
        lst.append({"name": course.name, "i_id": i_id, "form": SavedMarkForm(instance=instance), "mode": True})
    return render(request, 'app/edit_marks.html', {"field_list": lst})


@login_required()
def mark_edit(request, i_id):
    # def mark_edit(request, i_id, mode):
    mode = True
    if request.method == 'POST':
        (instance, created) = SavedMark.objects.get_or_create(course_id=i_id, user=request.user, defaults={"mark": 2})
        form = SavedMarkForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return render(request, 'app/edit_mark.html',
                          {"name": instance.course.name, "success": True, "i_id": i_id, "form": form, "mode": True})
        return render(request, 'app/edit_mark.html',
                      {"name": instance.course.name, "i_id": i_id, "form": form, mode: "mode"})

#proponowaczka przedmiotow obieralnych, wybieramy pzredmioty z listy
#i zapuszczany algorytm regułowy z R-a


#proponowaczka przedmiotow obieralnych, wybieramy pzredmioty z listy
#i zapuszczany algorytm regułowy z R-a

#zakomentowalem bo obecny kod sie wywala na tej formatce
#a do tego widok ten zapisuje oceny do bazy danych
#skrypt analizujacy powinien pobierac oceny od aktualnie zalogowanego uzytkownika
#@login_required()
def grades(request):
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = GradesForm(request.POST)
        if form.is_valid():
            values = []
            for i in range(50):
                values.append(form.cleaned_data['subject' + str(i)])
            marks = []
            for v in values:
                marks += [int(v)]
            recommendSubjects = Predictions.getRecomSubStrategy2(marks)
            return render(
                request,
                'app/gradesResult.html',
                context_instance=RequestContext(request,
                                                {
                                                    'gotSub': [],
                                                    'recomSub': recommendSubjects,
                                                })
            )

    return render(
        request,
        'app/grades.html',
        context_instance=RequestContext(request,
                                        {
                                            'title': 'Oceny',
                                            'message': 'Wprowadz dane',
                                            'year': datetime.now().year,
                                            'GradesForm': GradesForm(),
                                        })
    )

def parseFormSet(formset):
    for form in formset.forms:
        formName = form.prefix + '-' + 'course'
        courseName = form.data[formName]
        try:
            course = Course.objects.get(name=courseName)
            form.data._mutable = True
            form.data[formName] = course.id
            form.data._mutable = False
        except Exception, e:
            print e
            pass

@login_required()
def gradesDynamic(request):
    success = False
    assert isinstance(request, HttpRequest)
    student = request.user
    if request.method == 'POST':
        formset = MarkFormSet(request.POST, request.FILES)
        formset_validate = MarkFormSet(request.POST, request.FILES)

        parseFormSet(formset_validate)
        if formset_validate.is_valid():
            #TODO
            return HttpResponse("OK!")
        else:

        parseFormSet(formset)
        if formset.is_valid():
            for form in formset.forms:
                #TODO
                pass
            success=True
    else:
        formset = MarkFormSet()
    return render(
        request,
        'app/gradesDynamic.html',
        context_instance=RequestContext(request,
                                        {
                                            'title': 'Oceny',
                                            'message': 'Wprowadz dane',
                                            'year': datetime.now().year,
                                            'formset': formset,
                                            'success': success
                                        })
    )

@login_required()
def gradesFilter(request):
    success = False
    assert isinstance(request, HttpRequest)
    query = request.GET.get('query')
    if query is None:
        return HttpResponse('')

    courses = [course.name for course in Course.objects.filter(name__icontains=query)]

    return HttpResponse(','.join(courses))


def oauth_init(request):
    request_token_url = 'https://usosapps.uw.edu.pl/services/oauth/request_token'
    callback_url = 'http://' + request.META['HTTP_HOST'] + '/oauth_callback'

    oauth_request = oauth.Request.from_consumer_and_token(consumer, http_url=request_token_url,
                                                          parameters={'oauth_callback': callback_url,
                                                                      'scopes': 'grades'})
    oauth_request.sign_request(oauth.SignatureMethod_PLAINTEXT(), consumer, None)
    response = requests.get(request_token_url, headers=oauth_request.to_header())
    request_token = dict(urlparse.parse_qsl(response.content))
    print(request_token.values())
    response = redirect(
        'https://usosapps.uw.edu.pl/services/oauth/authorize?oauth_token=%s' % request_token['oauth_token'])
    response.set_cookie('oauth_request_secret', request_token['oauth_token_secret'])
    return response


def oauth_callback(request):
    access_token_url = 'https://apps.usos.edu.pl/services/oauth/access_token'

    request_token_secret = request.COOKIES.get('oauth_request_secret', '')
    token = oauth.Token(request.GET['oauth_token'], request_token_secret)
    token.set_verifier(request.GET['oauth_verifier'])
    oauth_request = oauth.Request.from_consumer_and_token(consumer, http_url=access_token_url)
    oauth_request.sign_request(oauth.SignatureMethod_PLAINTEXT(), consumer, token)
    response = requests.get(access_token_url, headers=oauth_request.to_header())

    #####################
    # dlaczego jest 401 unauthorized i message:"invalid consumer"
    ######################
    print(response.status_code)
    access_token = dict(urlparse.parse_qsl(response.content))
    raise Exception(response.content)

    ##################

    resource_url = 'https://usosapps.uw.edu.pl/services/grades/course_edition'

    token = oauth.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
    oauth_request = oauth.Request.from_consumer_and_token(consumer, http_url=resource_url)
    oauth_request.sign_request(oauth.SignatureMethod_PLAINTEXT(), consumer, None)
    print(oauth_request.viewkeys())

    # get the resource
    #response = requests.get(resource_url, headers=oauth_request.to_header())
    raise Exception('lol')
    return HttpResponse('lol')
