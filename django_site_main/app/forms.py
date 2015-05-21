"""
Definition of forms.
"""

from django import forms
from django.forms import ChoiceField, ModelForm, TextInput, Select, formset_factory
from django.utils.safestring import mark_safe

from models import *


# class BootstrapAuthenticationForm(AuthenticationForm):
# """Authentication form which uses boostrap CSS."""
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


class MarkForm(ModelForm):
    class Meta:
        model=Mark
        fields=['course', 'mark']
        widgets = {
            'course': TextInput(attrs={'class': 'course-input',}),
            'mark': Select(attrs={'class': 'mark-select',})

        }


MarkFormSet = formset_factory(MarkForm, extra=1)


class SavedMarkForm(forms.ModelForm):
    class Meta:
        model = SavedMark
        fields = ['mark']


class GradeField(forms.ChoiceField):
    marks = [(0, 'brak'), (4, '2'), (6, '3'), (7, '3.5'), (8, '4'), (9, '4.5'), (10, '5'), (11, '5!')]

    def __init__(self, choices=marks, required=True,
                 widget=None, label=None, initial=None, help_text='', *args, **kwargs):
        super(ChoiceField, self).__init__(required=required, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer),
                                          label=label,
                                          initial=0, help_text=help_text, *args, **kwargs)
        self.choices = choices


class GradesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(GradesForm, self).__init__(*args, **kwargs)
        subjects = Course.objects.all()[0:50]
        i = 0
        for s in subjects:
            self.fields['subject' + str(i)] = GradeField(label=s.name)
            i += 1

    def as_p(self):
        return self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; %(field)s%(help_text)s</p><hr>',
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)


    '''przedmiot_ob_1 = GradeField(label='Przedmiot obowiazkowy 1')
    przedmiot_ob_2 = GradeField(label='Przedmiot obowiazkowy 2')
    przedmiot_ob_3 = GradeField(label='Przedmiot obowiazkowy 3')
    przedmiot_ob_4 = GradeField(label='Przedmiot obowiazkowy 4')
    przedmiot_ob_5 = GradeField(label='Przedmiot obowiazkowy 5')
    przedmiot_ob_6 = GradeField(label='Przedmiot obowiazkowy 6')
    przedmiot_ob_7 = GradeField(label='Przedmiot obowiazkowy 7')
    przedmiot_ob_8 = GradeField(label='Przedmiot obowiazkowy 8')
    przedmiot_ob_9 = GradeField(label='Przedmiot obowiazkowy 9')
    przedmiot_ob_10 = GradeField(label='Przedmiot obowiazkowy 10')
    przedmiot_ob_11 = GradeField(label='Przedmiot obowiazkowy 11')
    przedmiot_ob_12 = GradeField(label='Przedmiot obowiazkowy 12')
    przedmiot_ob_13 = GradeField(label='Przedmiot obowiazkowy 13')
    przedmiot_ob_14 = GradeField(label='Przedmiot obowiazkowy 14')
    przedmiot_ob_15 = GradeField(label='Przedmiot obowiazkowy 15')
    przedmiot_ob_16 = GradeField(label='Przedmiot obowiazkowy 16')
    przedmiot_ob_17 = GradeField(label='Przedmiot obowiazkowy 17')
    przedmiot_ob_18 = GradeField(label='Przedmiot obowiazkowy 18')
    przedmiot_ob_19 = GradeField(label='Przedmiot obowiazkowy 19')
    przedmiot_ob_20 = GradeField(label='Przedmiot obowiazkowy 20')
    przedmiot_ob_21 = GradeField(label='Przedmiot obowiazkowy 21')
    przedmiot_ob_22 = GradeField(label='Przedmiot obowiazkowy 22')
    przedmiot_ob_23 = GradeField(label='Przedmiot obowiazkowy 23')
    przedmiot_ob_24 = GradeField(label='Przedmiot obowiazkowy 24')
    przedmiot_ob_25 = GradeField(label='Przedmiot obowiazkowy 25')
    przedmiot_ob_26 = GradeField(label='Przedmiot obowiazkowy 26')
    przedmiot_ob_27 = GradeField(label='Przedmiot obowiazkowy 27')
    przedmiot_ob_28 = GradeField(label='Przedmiot obowiazkowy 28')
    przedmiot_ob_29 = GradeField(label='Przedmiot obowiazkowy 29')
    przedmiot_ob_30 = GradeField(label='Przedmiot obowiazkowy 30')'''
