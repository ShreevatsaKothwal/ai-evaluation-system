from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            "class": "form-input",
            "placeholder": "Username"
        })

        self.fields['email'].widget.attrs.update({
            "class": "form-input",
            "placeholder": "Email"
        })

        self.fields['password1'].widget.attrs.update({
            "class": "form-input",
            "placeholder": "Password"
        })

        self.fields['password2'].widget.attrs.update({
            "class": "form-input",
            "placeholder": "Confirm Password"
        })