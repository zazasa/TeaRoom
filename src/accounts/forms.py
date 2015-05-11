from __future__ import unicode_literals
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field
# from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from authtools import forms as authtoolsforms
from django.contrib.auth import forms as authforms
from django.core.urlresolvers import reverse

# from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from django.utils.translation import ugettext_lazy as _, ugettext

User = get_user_model()


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["username"].widget.input_type = "email"  # ugly hack

        self.helper.layout = Layout(Field('username', placeholder="Enter Email", autofocus=""),
                                    Field('password', placeholder="Enter Password"),
                                    HTML('<a href="{}">Forgot Password?</a>'.format(
                                         reverse("accounts:password-reset"))),
                                    Field('remember_me'),
                                    Submit('sign_in', 'Log in',
                                           css_class="btn btn-lg btn-primary btn-block"),
                                    )

# Original Template Form
# class SignupForm(authtoolsforms.UserCreationForm):

#     def __init__(self, *args, **kwargs):
#         super(SignupForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.fields["email"].widget.input_type = "email"  # ugly hack

#         self.helper.layout = Layout(
#             Field('email', placeholder="Enter Email", autofocus=""),
#             Field('name', placeholder="Enter Full Name"),
#             Field('password1', placeholder="Enter Password"),
#             Field('password2', placeholder="Re-enter Password"),
#             Submit('sign_up', 'Sign up', css_class="btn-warning"),
#             )


class SignupForm(forms.ModelForm):

    """
    A form for creating new users.
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SignupForm, self).__init__(*args, **kwargs)

        def validate_uniqueness_of_username_field(value):
            # Since User.username is unique, this check is redundant,
            # but it sets a nicer error message than the ORM. See #13147.
            try:
                User._default_manager.get_by_natural_key(value)
            except User.DoesNotExist:
                return value
            raise forms.ValidationError(self.error_messages['duplicate_username'] %
                                        {'username': User.USERNAME_FIELD})

        self.fields[User.USERNAME_FIELD].validators.append(
            validate_uniqueness_of_username_field)

        self.helper = FormHelper()
        self.fields["email"].widget.input_type = "email"  # ugly hack

        self.helper.layout = Layout(Field('email', placeholder="Enter Email", autofocus=""),
                                    Field('name', placeholder="Enter Full Name"),
                                    Submit('sign_up', 'Sign up', css_class="btn-warning"),)

    class Meta:
        model = User
        fields = (User.USERNAME_FIELD,) + tuple(User.REQUIRED_FIELDS)

    def save(self, commit=True):

        subject_template_name = 'accounts/emails/registration_email_subject.txt'
        email_template_name = 'accounts/emails/registration_email.txt'

        user = super(SignupForm, self).save(commit=False)
        user.is_active = False
        user.set_unusable_password()
        user.send_mail(self.request, subject_template_name, email_template_name)

        if commit:
            user.save()
        return user


class PasswordChangeForm(authforms.PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(Field('old_password', placeholder="Enter old password", autofocus=""),
                                    Field('new_password1', placeholder="Enter new password"),
                                    Field('new_password2', placeholder="Enter new password (again)"),
                                    Submit('pass_change', 'Change Password', css_class="btn-warning"),
                                    )


class PasswordResetForm(authtoolsforms.FriendlyPasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(Field('email', placeholder="Enter email", autofocus=""),
                                    Submit('pass_reset', 'Reset Password', css_class="btn-warning"),
                                    )


class FirstPasswordSetForm(authtoolsforms.OldPasswordResetForm):
    error_messages = dict(getattr(authtoolsforms.OldPasswordResetForm, 'error_messages', {}))
    error_messages['unknown'] = _("This email address doesn't have an "
                                  "associated user account. Are you "
                                  "sure you've registered?")

    def __init__(self, *args, **kwargs):
        super(FirstPasswordSetForm, self).__init__(*args, **kwargs)

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        Overload default behavior that:
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.

        """
        active_users = get_user_model()._default_manager.filter(is_active=False, email__iexact=email)
        return (u for u in active_users)

    def clean_email(self):
        # print super(FirstPassordSetForm, self).is_valid()
        # print self.cleaned_data
        # print super(FirstPassordSetForm, self).cleaned_data

        # super_clean_email = getattr(
        #     super(FirstPassordSetForm, self), 'clean_email', None)
        # if callable(super_clean_email):  # Django == 1.5
        #     # Django 1.5 sets self.user_cache
        #     return super_clean_email()

        # Simulate Django 1.5 behavior in Django >= 1.6.
        # This is not as efficient as in Django 1.5, since clean_email() and
        # save() will be running the same query twice.
        # Whereas Django 1.5 just caches it.
        email = self.cleaned_data['email']
        qs = User._default_manager.filter(is_active=False, email__iexact=email)
        results = [user for user in qs]
        if not results:
            raise forms.ValidationError(self.error_messages['unknown'])
        return email


class SetPasswordForm(authforms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(Field('new_password1', placeholder="Enter new password", autofocus=""),
                                    Field('new_password2', placeholder="Enter new password (again)"),
                                    Submit('pass_change', 'Change Password', css_class="btn-warning"),
                                    )
