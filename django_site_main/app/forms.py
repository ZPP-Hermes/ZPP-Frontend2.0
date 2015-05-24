"""
Definition of forms.
"""

from django import forms
from django.forms import widgets, ChoiceField
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from django.forms.formsets import formset_factory
from app.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from models import Course

# class BootstrapAuthenticationForm(AuthenticationForm):
#     """Authentication form which uses boostrap CSS."""
#     username = forms.CharField(max_length=254,
#                                widget=forms.TextInput({
#                                    'class': 'form-control',
#                                    'placeholder': 'User name'}))
#     password = forms.CharField(label=_("Password"),
#                                widget=forms.PasswordInput({
#                                    'class': 'form-control',
#                                    'placeholder':'Password'}))

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
            return mark_safe(u'\n'.join([u'%s &nbsp; &nbsp;' % w for w in self]))


'''class MarkForm(ModelForm):
    class Meta:
        model=Mark
        fields=['mark', 'course']


MarkFormSet = formset_factory(MarkForm, extra=1)
'''
class GradeField(forms.ChoiceField):

    marks = [(0,'brak'), (4,'2'), (6,'3'), (7,'3.5'), (8,'4'), (9,'4.5'), (10,'5'), (11,'5!')]
    def __init__(self, choices=marks, required=True,
                 widget=None, label=None, initial=None, help_text='', *args, **kwargs):
        super(ChoiceField, self).__init__(required=required, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), label=label,
                                        initial=0, help_text=help_text, *args, **kwargs)
        self.choices = choices

class GradesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        algsSub = [(1,'strategia wykorzystujaca algorytm regulowy'),(2,'lista priorytetowa najlatwiejszych przedmiotow'),
                  (3,'dobierz w sposob losowy'),(4,'strategia najblizszych sasiadow')]
        algsSem = [(1,'strategia wykorzystujaca algorytm lasow losowych'),(2,'strategia najblizszych sasiadow')]
        super(GradesForm, self).__init__(*args, **kwargs)
        subjects = Course.objects.all()[0:50]
        i = 0
        for s in subjects:
            self.fields['subject' + str(i)] = GradeField(label=s.name)
            i += 1
        self.fields['algorithmSub'] = forms.MultipleChoiceField(required=False,
        widget=forms.CheckboxSelectMultiple, choices=algsSub,label="Wybierz algorytm predykcji przedmiotow")
        self.fields['algorithmSem'] = forms.MultipleChoiceField(required=False,
        widget=forms.CheckboxSelectMultiple, choices=algsSem,label="Wybierz algorytm predykcji seminariow")

    def as_p(self):
        return self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; %(field)s%(help_text)s</p><hr>',
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)

