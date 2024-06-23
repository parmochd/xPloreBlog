from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, get_user
# https://pypi.org/project/django-recaptcha/
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.utils.translation import gettext_lazy as _


# Create your forms here.

class NewUserForm(UserCreationForm):
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)

    error_messages = {
        'password_mismatch': _("The passwords you entered do not match. Please make sure your passwords match and try again."),
    }

    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['password1'].label = 'password1 label'
        # self.fields['password2'].label = 'password2 label'

        self.fields['name'].help_text = 'Required. 200 characters or fewer'
        self.fields['password1'].help_text = 'Your password must be distinct from personal information, contain at least 8 characters, not be a commonly used password, and not consist entirely of numbers.'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name_parts = name.split()
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
            self.cleaned_data['first_name'] = first_name
            self.cleaned_data['last_name'] = last_name
        return name

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.is_active = False

        # Populate first_name and last_name from name field
        name = self.cleaned_data.get('name')
        if name:
            name_parts = name.split()
            user.first_name = name_parts[0]
            user.last_name = " ".join(name_parts[1:]) if len(
                name_parts) > 1 else ""

        if commit:
            user.save()
        return user


# Login Form

class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    username = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label="Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


# Set Password Form


class SetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _("The passwords you entered do not match. Please make sure your passwords match and try again."),
    }

    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


# Reset Password
class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


# Change Password
class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class PostForm(forms.ModelForm):
    # content = forms.CharField(widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['tag'].widget.attrs['class'] = 'form-control'
        self.fields['author'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Post
        fields = "__all__"
        exclude = ['slug', 'status', 'created_on',
                   'created_by', 'updated_by', 'updated_on']
