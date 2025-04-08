from django import forms

from mailing.models import Mailing, Blog


class MailingForm(forms.ModelForm):
    start_sending = forms.DateTimeField(
        input_formats=['%d.%m.%Y %H:%M', '%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M', attrs={'type': 'datetime-local'})
    )
    end_sending = forms.DateTimeField(
        input_formats=['%d.%m.%Y %H:%M', '%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M', attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Mailing
        exclude = ['status', 'owner']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ['creation_date', 'views']
