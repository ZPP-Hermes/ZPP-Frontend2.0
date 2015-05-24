# coding=utf-8
"""
Definition of views.
"""

from datetime import datetime
import urlparse

from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.core.urlresolvers import reverse
from app.forms import GradesForm
import urlparse
import oauth2 as oauth
import requests
import numpy as np

from forms import *
from models import *
import Predictions

consumer = oauth.Consumer(key='uvTtX63RWFaCf9pAxdtT', secret='5Jn3t9KNVMvSCeBtREX3nCvcKAnL55UrJKbcTvxD')


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


'''def login(request):

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/login.html',
        context_instance = RequestContext(request,
        {
            'title':'Logowanie',
            'year':datetime.now().year,
        })
    )'''


#proponowaczka przedmiotow obieralnych, wybieramy pzredmioty z listy
#i zapuszczany algorytm regułowy z R-a


#proponowaczka przedmiotow obieralnych, wybieramy pzredmioty z listy
#i zapuszczany algorytm regułowy z R-a

#zakomentowalem bo obecny kod sie wywala na tej formatce
#a do tego widok ten zapisuje oceny do bazy danych
#skrypt analizujacy powinien pobierac oceny od aktualnie zalogowanego uzytkownika
#@login_required()

#troche ifowo elsowy ale na razie nie wiem jak lepiej zrobic wybor
#konkretnych algorytmow (zeby wyswietlac uzytkownikowi tylko wybrane)
def grades(request):
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = GradesForm(request.POST)
        if form.is_valid():
            values = []
            for i in range(50):
                values.append(form.cleaned_data['subject' + str(i)])
            marks = map(int, values)
            selectedAlg = map(int, form.cleaned_data['algorithm'])
            recommendSubjects1 = []
            recommendSubjects2 = []
            recommendSubjects3 = []
            recommendSubjects4 = []
            recSubNames1 = []
            recSubNames2 = []
            recSubNames3 = []
            recSubNames4 = []
            algorytmy = []
            if (1 in selectedAlg):
                algorytmy.append(1)
                recommendSubjects1 = Predictions.getRecomSubStrategy1(marks)
                for i in range(0,len(recommendSubjects1)):
                    id_course = recommendSubjects1[i]
                    course = Course.objects.get(pk=id_course)
                    recSubNames1.append((course.name,course.url))
            else:
                algorytmy.append(None)
            if (2 in selectedAlg):
                algorytmy.append(2)
                recommendSubjects2 = Predictions.getRecomSubStrategy2(marks)
                for i in range(0,len(recommendSubjects2)):
                    id_course = recommendSubjects2[i]
                    course = Course.objects.get(pk=id_course)
                    link = course.url
                    recSubNames2.append((course.name,course.url))
            else:
                algorytmy.append(None)
            if (3 in selectedAlg):
                algorytmy.append(3)
                recommendSubjects3 = Predictions.getRecomSubStrategy3(marks)
                for i in range(0,len(recommendSubjects3)):
                    id_course = recommendSubjects3[i]
                    course = Course.objects.get(pk=id_course)
                    recSubNames3.append((course.name,course.url))
            else:
                algorytmy.append(None)
            if (4 in selectedAlg):
                algorytmy.append(4)
                recommendSubjects4 = Predictions.getRecomSubStrategy4(marks)
                for i in range(0,len(recommendSubjects4)):
                    id_course = recommendSubjects4[i]
                    course = Course.objects.get(pk=id_course)
                    recSubNames4.append((course.name,course.url))
            else:
                algorytmy.append(None)
            return render(
                request,
                'app/gradesResult.html',
                context_instance=RequestContext(request,
                                                {
                                                    'alg': algorytmy,
                                                    'recomSub1': recSubNames1,
                                                    'recomSub2': recSubNames2,
                                                    'recomSub3': recSubNames3,
                                                    'recomSub4': recSubNames4,
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


'''@login_required()
def grades(request):
    success = False
    assert isinstance(request, HttpRequest)
    student = request.user
    if request.method == 'POST':
        formset = MarkFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset.forms:
                tmpform = form.save(commit=False)
                tmpform.student = student
                if tmpform.course:
                    tmpform.save()
            success=True
    else:
        courses = list(Course.objects.all())
        def in_f(item) :
            return {"course": item}
        _initial = map(in_f, courses)
        formset = MarkFormSet(initial=_initial)
    return render(
        request,
        'app/grades.html',
        context_instance=RequestContext(request,
                                        {
                                            'title': 'Oceny',
                                            'message': 'Wprowadz dane',
                                            'year': datetime.now().year,
                                            'formset': formset,
                                            'success': success
                                        })
    )'''


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
