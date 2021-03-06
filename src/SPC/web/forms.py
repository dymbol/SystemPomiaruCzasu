from django import forms
from web.models import Track


class EditRace(forms.Form):
    track = forms.ModelChoiceField(queryset=Track.objects.all())

    def __init__(self, *args, **kwargs):
        race_id = kwargs.pop('race_id', None)
        super(EditRace, self).__init__(*args, **kwargs)

        self.fields['track'].label = "Trasa"

        if race_id:
            self.fields['track'].queryset = Track.objects.filter(race__id=race_id)

