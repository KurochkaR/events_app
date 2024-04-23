from django import forms
from django.contrib.auth.forms import UserCreationForm

from authorization.models import CustomUser


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = ''
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = ''
            if field == 'password1' or field == 'password2':
                self.fields[field].widget.attrs['placeholder'] = 'Password'
            else:
                self.fields[field].widget.attrs['placeholder'] = field.title

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.username = user.email = self.cleaned_data['email']
        if commit:
            user.save()
            return user
