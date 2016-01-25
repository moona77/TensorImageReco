from django import forms

class SearchForm(forms.Form):
    '''
    Text searching form.
    '''
    # pylint: disable=C0103
    q = forms.CharField(
        label='Query',
        min_length=1,
        required=False,
    )
    period = forms.ChoiceField(
        label='Period',
        required=False,
        choices=(
            ('1w', '1 week'),
            ('1m', '1 month'),
            ('3m', '3 months'),
        ),
        initial=False
    )
    every = forms.BooleanField(
        label='Everything',
        required=False,
        initial=True
    )
    pol = forms.BooleanField(
        label='Politic',
        required=False,
        initial=False
    )
    pub = forms.BooleanField(
        label='Public Office',
        required=False,
        initial=False
    )
    ent = forms.BooleanField(
        label='Enterprise',
        required=False,
        initial=False
    )
    univ = forms.BooleanField(
        label='Univ/Professor',
        required=False,
        initial=False
    )


