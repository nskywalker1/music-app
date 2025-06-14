from django.contrib.auth.forms import UserCreationForm, \
    AuthenticationForm
from .models import CustomUser
from django import forms
from django.contrib.auth import authenticate


class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False,
                          label='Artist bio')

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'avatar', 'bio', 'password1', 'password2', 'role')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1 and len(password1) < 8:
            self.add_error('password1', 'Minimum 8 characters')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        return password2


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError('Invalid email or password')
            return self.cleaned_data
