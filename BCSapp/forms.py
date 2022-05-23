from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Transaction


class TxDescription(forms.ModelForm):
    description = forms.CharField(required=False, label='Описание', initial='')

    class Meta:
        model = Transaction
        fields = ['txid', 'description',]

    def __init__(self, *args, **kwargs):
        super(TxDescription, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['txid'].widget.attrs['readonly'] = True


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))



