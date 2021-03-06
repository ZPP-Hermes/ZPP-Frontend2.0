# coding=utf-8
"""
Definition of forms.
"""

from django import forms
from django.forms import ChoiceField, ModelForm, TextInput, Select, formset_factory, RadioSelect
from django.utils.safestring import mark_safe

from models import *


# class BootstrapAuthenticationForm(AuthenticationForm):
# """Authentication form which uses boostrap CSS."""
# username = forms.CharField(max_length=254,
# widget=forms.TextInput({
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
    # _algorithmSub = [(1, 'strategia wykorzystujaca algorytm regulowy'),
    #                  (2, 'lista priorytetowa najlatwiejszych przedmiotow'),
    #                  (3, 'dobierz w sposob losowy'), (4, 'strategia najblizszych sasiadow')]
    # _algorithmSem = [(1, 'strategia wykorzystujaca algorytm lasow losowych'), (2, 'strategia najblizszych sasiadow')]
    #
    # algorithmSub = forms.MultipleChoiceField(required=False,
    #                                          widget=forms.CheckboxSelectMultiple, choices=_algorithmSub,
    #                                          label="Wybierz algorytm predykcji przedmiotow")
    # algorithmSem = forms.MultipleChoiceField(required=False,
    #                                          widget=forms.CheckboxSelectMultiple, choices=_algorithmSem,
    #                                          label="Wybierz algorytm predykcji seminariow")
    course_display = forms.CharField(max_length=100)

    class Meta:
        model = Mark
        fields = ['course', 'course_display', 'mark']
        widgets = {
            # 'course': forms.Input(attrs={'class': 'course-input', }),
            # 'course_display': forms.TextInput(attrs={'class': 'course-display', }),
            'mark': Select(attrs={'class': 'mark-select', })

        }

    def __init__(self, *args, **kwargs):
        super(MarkForm, self).__init__(*args, **kwargs)
        self.fields['course_display'].label = "Przedmiot"
        self.fields['course_display'].widget = forms.TextInput(attrs={'class': 'course-display', })

        self.fields['course'].widget = TextInput(attrs={'class': 'course-input', })
        self.fields['mark'].label = "Ocena"
        self.empty_permitted = False


MarkFormSet = formset_factory(MarkForm)


class SavedMarkForm(forms.ModelForm):
    class Meta:
        model = SavedMark
        fields = ['mark']
        widgets = {
            'mark': RadioSelect()
        }


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
        algsSub = [(1, 'strategia wykorzystujaca algorytm regulowy'),
                   (2, 'lista priorytetowa najlatwiejszych przedmiotow'),
                   (3, 'dobierz w sposob losowy'), (4, 'strategia najblizszych sasiadow')]
        algsSem = [(1, 'strategia wykorzystujaca algorytm lasow losowych'), (2, 'strategia najblizszych sasiadow')]
        subs = [(31,"Zaawansowane systemy operacyjne"), (32,"Programowanie mikrokontrolerow"), (33,"Kompresja danych"),
                    (34,"Przetwarzanie duzych danych"),
                    (35,"Programowanie w logice"), (36,"Wstęp do biologii obliczeniowej"),
                    (37,"Zaawansowane bazy danych"), (38,"Systemy uczące się"), (39,"Sztuczna inteligencja i systemy doradcze"),
                    (40,"Data mining"), (41,"Algorytmika"),
                    (42,"Algorytmy tekstowe"), (43,"Weryfikacja wspomagana komputerowo"),
                    (44,"Wnioskowanie w serwisach i systemach informatycznych"),
                    (45,"Teoria informacji"), (46,"Kryptografia"),
                    (47,"Matematyka obliczeniowa 2"), (48,"Statystyka 2"),
                    (49,"Rachunek prawdopodobienstwa 2"), (50,"Optymalizacja 1")]
        sems = [(51,"Systemy rozproszone"), (52,"Języki programowania"), (53,"Zagadnienia programowania obiektowego"),
                (54,"Wybrane aspekty inżynierii oprogramowania"),
                (55,"Analiza, wizualizacja i optymalizacja oprogramowania"), (56,"Innowacyjne zastosowania informatyki"),
                (57,"Molekularna biologia obliczeniowa"), (58,"Algorytmika"),
                (59,"Metody numeryczne"),(60,"Matematyka w informatyce")]
        super(GradesForm, self).__init__(*args, **kwargs)
        subjects = Course.objects.all()[0:50]
        i = 0
        for s in subjects:
            self.fields['subject' + str(i)] = GradeField(label=s.name)
            i += 1
        self.fields['algorithmSub'] = forms.MultipleChoiceField(required=False,
                                                                widget=forms.CheckboxSelectMultiple, choices=algsSub,
                                                                label="Wybierz algorytm predykcji przedmiotow")
        self.fields['semSubject'] = forms.ChoiceField(required=False,choices=sems,
                                                                label="Wybierz seminarium do predykcji przedmiotow")
        self.fields['algorithmSem'] = forms.MultipleChoiceField(required=False,
                                                                widget=forms.CheckboxSelectMultiple, choices=algsSem,
                                                                label="Wybierz algorytm predykcji seminariow")
        self.fields['markSubject'] = forms.ChoiceField(required=False,choices=subs,
                                                                label="Wybierz przedmiot do predykcji oceny")

    def as_p(self):
        return self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; %(field)s%(help_text)s</p><hr>',
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)

