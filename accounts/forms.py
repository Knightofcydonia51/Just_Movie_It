from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'age', 'profile')
        widgets = {
            'age': forms.NumberInput(attrs={'min': 0, 'max':200})
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('followings', 'age', 'username',)
        widgets = {
            'score': forms.NumberInput(attrs={'min': 0})
        }

