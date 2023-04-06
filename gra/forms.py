from django import forms

class CreateNewSession(forms.Form):
    game_name = forms.CharField(label="Name", max_length=200)

