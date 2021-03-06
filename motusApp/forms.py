from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.PasswordInput()
    next_url = forms.HiddenInput()
