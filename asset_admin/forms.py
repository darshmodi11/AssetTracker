from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100,
                            error_messages=
                            {'required': 'Please enter your email address.'}
                            )
    password = forms.CharField(widget=forms.PasswordInput(),
                               error_messages=
                               {'required': 'Please enter your password.'}
                               )
    remember_me = forms.BooleanField(required=False)
