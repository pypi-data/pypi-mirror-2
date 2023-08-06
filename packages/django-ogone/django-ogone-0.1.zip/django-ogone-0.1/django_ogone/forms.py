from django import forms
from django_ogone import settings as ogone_settings

class OgoneForm(forms.Form):
    """ Dynamic ogone form """


    def __init__(self, initial_data, *args, **kwargs):
        super(OgoneForm, self).__init__(*args, **kwargs)
        for name, value in initial_data.items():
            self.fields[name] = forms.CharField(widget=forms.HiddenInput,
                initial=value)