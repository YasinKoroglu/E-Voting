import string
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import Account, MyAccountManager


class RegistrationForm(UserCreationForm):
    
    ident = forms.IntegerField(validators=[RegexValidator(regex='^.{11}$', message='Length has to be 11', code='nomatch')] ,help_text='Required. Add a valid S.S.N address.')
    
    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2','ident','firstname','lastname' )

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        

        return password1    



class nonRegisteredUseVoteForm(forms.Form):
    ssn = forms.IntegerField()
    vote_code = forms.CharField(max_length=100)


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")






class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'username', )

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)