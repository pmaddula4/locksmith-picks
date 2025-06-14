from django import forms
from .models import MailingListSubscriber


class MailingListForm(forms.ModelForm):
    model = MailingListSubscriber
    fields = ['first_name', 'last_name', 'favorite_team', 'email']