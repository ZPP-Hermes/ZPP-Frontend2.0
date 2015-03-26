"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.core.urlresolvers import reverse
from app.forms import GradesForm

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

def grades(request):

    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = GradesForm(request.POST)
        if form.is_valid():
            # TODO
            return HttpResponseRedirect(reverse('app:home'))

    return render(
        request,
        'app/grades.html',
        context_instance = RequestContext(request,
        {
            'title':'Oceny',
            'message':'Wprowadź dane',
            'year':datetime.now().year,
            'gradesForm': GradesForm(),
        })
    )
