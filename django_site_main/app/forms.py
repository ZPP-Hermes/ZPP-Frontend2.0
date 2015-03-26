"""
Definition of forms.
"""

from django import forms
from django.forms import widgets, ChoiceField
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

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

class GradeField(forms.ChoiceField):

    def __init__(self, choices=[(x, x) for x in range(2, 7)], required=True,
                 widget=None, label=None, initial=None, help_text='', *args, **kwargs):
        super(ChoiceField, self).__init__(required=required, widget=widget, label=label,
                                        initial=initial, help_text=help_text, *args, **kwargs)
        self.choices = choices

class GradesForm(forms.Form):
    grade1 = GradeField(label='Przedmiot 1')
    grade2 = GradeField(label='Przedmiot 2')
    grade3 = GradeField(label='Przedmiot 3')
    grade4 = GradeField(label='Przedmiot 4')
    grade5 = GradeField(label='Przedmiot 5')
    grade6 = GradeField(label='Przedmiot 6')
    grade7 = GradeField(label='Przedmiot 7')
    grade8 = GradeField(label='Przedmiot 8')
    grade9 = GradeField(label='Przedmiot 9')
    grade10 = GradeField(label='Przedmiot 10')