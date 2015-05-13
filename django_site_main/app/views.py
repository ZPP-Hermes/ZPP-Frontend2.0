# coding=utf-8
"""
Definition of views.
"""

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from app.forms import GradesForm
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime
import urlparse
import oauth2 as oauth
import requests
import pyRserve
import numpy as np
from models import Mark
import Rscripts

consumer = oauth.Consumer(key='uvTtX63RWFaCf9pAxdtT', secret='5Jn3t9KNVMvSCeBtREX3nCvcKAnL55UrJKbcTvxD')
#przygotowywanie skryptow R-owych
conn = pyRserve.connect()
conn.r(Rscripts.Rscript.arules)
# tu będziemy chcieli wczytywać dane z bazy
#conn.r.data = prepData()

#funkcja bioraca dane z bazy i przerabiajaca na macierz do R, ja jeszcze trzeba przerobic
def prepData():
    dataPr = Mark.objects.all()
    dataPr = dataPr.values_list()
    colNum = len(dataPr[1])
    dataList = []
    for i in range(colNum):
        dataList += [id[i] for id in dataPr]
    dataR = np.array(dataList)
    dataR.shape = (colNum,len(dataList)/colNum)
    return dataR

def home(request):

    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Strona domowa',
            'year':datetime.now().year,
        })
    )

def login(request):

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/login.html',
        context_instance = RequestContext(request,
        {
            'title':'Logowanie',
            'year':datetime.now().year,
        })
    )

#proponowaczka przedmiotow obieralnych, wybieramy pzredmioty z listy
#i zapuszczany algorytm regułowy z R-a
def grades(request):

    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = GradesForm(request.POST)
        if form.is_valid():
            values = form.cleaned_data.values()
            marks = []
            for v in values:
                marks += [int(v)]
            conn.r.gotMarks = marks
            gotSub = conn.r('which(gotMarks>0)')
            recommendSubjects = conn.r('getRecomSub(which(gotMarks>0),0.5)')
            return render(
                request,
                'app/gradesResult.html',
                context_instance = RequestContext(request,
                {
                    'gotSub':gotSub,
                    'recomSub':recommendSubjects,
                })
            )

    return render(
        request,
        'app/grades.html',
        context_instance = RequestContext(request,
        {
            'title':'Oceny',
            'message':'Wprowadz dane',
            'year':datetime.now().year,
            'gradesForm': GradesForm(),
        })
    )

def oauth_init(request):
    request_token_url = 'https://usosapps.uw.edu.pl/services/oauth/request_token'
    callback_url = 'http://' + request.META['HTTP_HOST']+'/oauth_callback'

    oauth_request = oauth.Request.from_consumer_and_token(consumer, http_url=request_token_url, parameters={'oauth_callback':callback_url, 'scopes':'grades'})
    oauth_request.sign_request(oauth.SignatureMethod_PLAINTEXT(), consumer, None)
    response = requests.get(request_token_url, headers=oauth_request.to_header())
    request_token = dict(urlparse.parse_qsl(response.content))
    print(request_token.values())
    response = redirect('https://usosapps.uw.edu.pl/services/oauth/authorize?oauth_token=%s' % request_token['oauth_token'])
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
