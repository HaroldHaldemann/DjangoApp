from django import forms

from reviews import models


class FollowForm(forms.Form):
    username = forms.CharField(max_length=63, label="Nom d'utlisateur")


class TicketForm(forms.ModelForm):
    title = forms.CharField(max_length=128, label="Titre")
    description = forms.CharField(max_length=2048, widget=forms.Textarea, label="Description")

    class Meta:
        model = models.Ticket
        fields = ['title', 'description']


class ReviewForm(forms.ModelForm):
    CHOICES = [
        ('0', '- 0'),
        ('1', '- 1'),
        ('2', '- 2'),
        ('3', '- 3'),
        ('4', '- 4'),
        ('5', '- 5'),
    ]
    headline = forms.CharField(max_length=128, label="Titre")
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label="Note")
    body = forms.CharField(max_length=8192, widget=forms.Textarea, label="Commentaire")

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
