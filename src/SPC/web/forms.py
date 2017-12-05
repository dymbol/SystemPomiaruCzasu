from django import forms
from web.models import Track


class EditRace(forms.Form):
    loop = forms.DecimalField(label='Zmiana Pętli')
    track = forms.ModelChoiceField(queryset=Track.objects.all())

    def __init__(self, *args, **kwargs):
        race_id = kwargs.pop('race_id', None)
        super(EditRace, self).__init__(*args, **kwargs)
        if race_id:
            self.fields['track'].queryset = Track.objects.filter(race__id=race_id)

