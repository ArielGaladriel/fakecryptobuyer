from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django import forms

from .models import CustomUser, CryptoData


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name',)

class Bin(forms.Form):
    model = CryptoData.objects.all()[1:11].values()
    crypto_name = ['default_value'] + [row['crypto_name'] for row in model]
    human_name = ['--Choose currency--'] + [row['human_name'] for row in model]
    choises = zip(crypto_name, human_name)
    currencies = forms.ChoiceField(choices = choises)
    quantity = forms.IntegerField(min_value=0, max_value=10000, initial=0, widget=forms.TextInput)