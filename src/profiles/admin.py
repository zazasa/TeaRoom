from __future__ import unicode_literals
from django.contrib import admin
from authtools.admin import NamedUserAdmin
from .models import Profile
from accounts.forms import FirstPasswordSetForm
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = Profile


class NewUserAdmin(NamedUserAdmin):
    inlines = [UserProfileInline]
    list_display = ('is_active', 'email', 'name', 'permalink',
                    'is_superuser', 'is_staff', 'signup_status')

    actions = ["accept_registration"]

    # 'View on site' didn't work since the original User model needs to
    # have get_absolute_url defined. So showing on the list display
    # was a workaround.
    def permalink(self, obj):
        url = reverse("profiles:show", kwargs={"slug": obj.profile.slug})
        # Unicode hex b6 is the Pilcrow sign
        return '<a href="{}">{}</a>'.format(url, '\xb6')
    permalink.allow_tags = True

    def signup_status(self, obj):
        if obj.is_superuser:
            return 'N/A'
        else:
            return obj.status
    signup_status.admin_order_field = 'status'

    def accept_registration(self, request, queryset):
        rows_updated = queryset.update(status='accepted')
        for user in queryset:
            self.set_first_password(user, request)
        # import pdb; pdb.set_trace()
        if rows_updated == 1:
            message_bit = "1 user was"
        else:
            message_bit = "%s users were" % rows_updated
        self.message_user(request, "%s successfully marked as accepted." % message_bit)

    def set_first_password(self, user, request):
        subject_template_name = 'accounts/emails/acceptance_email_subject.txt'
        email_template_name = 'accounts/emails/acceptance_email.txt'
        # from_email = None

        # import pdb; pdb.set_trace()

        context = {
            'protocol': 'https',
        }
        form = FirstPasswordSetForm({'email': user.email})
        form.is_valid()
        return form.save(request=request, subject_template_name=subject_template_name, email_template_name=email_template_name, context)


admin.site.register(User, NewUserAdmin)
