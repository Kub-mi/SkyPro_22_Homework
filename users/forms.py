from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from users.models import CustomUser



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email",)


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("avatar", "phone", "country")
