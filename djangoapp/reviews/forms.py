from django import forms


class FollowForm(forms.Form):
    username = forms.CharField(max_length=63, label="Nom d'utlisateur")
