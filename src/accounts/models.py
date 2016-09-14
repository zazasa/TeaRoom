from django.db import models
from django.utils.text import ugettext_lazy as _
from authtools.models import AbstractNamedUser
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from TeaRoom.settings import Site


class User(AbstractNamedUser):

    STATUS_LIST = (
        ('untreated', _('Untreated yet')),
        ('accepted', _('Registration has accepted')),
        ('rejected', _('Registration has rejected')),
        ('registered', _('User is registered')),
    )

    status = models.CharField(_('status'), max_length=10, db_column='status',
                              choices=STATUS_LIST, default='untreated',
                              editable=False)

    def send_mail(self, request, subject_template_name, email_template_name,
                  html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        from_email = None
        to_email = self.email
        context = self.get_context()

        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_context(self):
        context = {
            'user': self.name,
            'email': self.email,
            'site': Site,
            # 'domain': domain,
            # 'site_name': site_name,
            # 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            # 'token': token_generator.make_token(user),
            'protocol': 'https',  # if use_https else 'http',
        }

        return context
