from django import forms
from .models import MailingListSubscriber


class MailingListForm(forms.ModelForm):
    class Meta:
        model = MailingListSubscriber
        fields = ['first_name', 'last_name', 'favorite_team', 'email']