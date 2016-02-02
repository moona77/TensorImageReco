#-*- coding: utf-8 -*-
from django import forms

class SearchForm(forms.Form):
    '''
    Text searching form.
    '''
    # pylint: disable=C0103
    image = forms.ImageField(
        label='이미지',
        #required=True,

    )



