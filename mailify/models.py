from django.core.exceptions import ValidationError
from django.db import models
from django.template import loader, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from fields import SeparatedValuesField
from settings import *


class MailifyMessage(models.Model):
    NOW = 0
    DELAY = 1
    DEFER = 2
    SEND_CHOICES = (
        (NOW, _(u'Now')),
        (DELAY, _(u'Delay')),
        (DEFER, _(u'Defer')),
    )
    description = models.CharField(
        verbose_name = _(u'Description'),
        max_length = 250,
        default = _(u'Message')
    )
    sender = models.CharField(
        verbose_name = _(u'Sender'),
        max_length = 254,
        default = DEFAULT_FROM_EMAIL,
        blank = True,
        null = True
    )
    recipients = SeparatedValuesField(
        verbose_name = _(u'Recipients')
    )
    subject_context = JSONField(
        verbose_name = _(u'Subject Context'),
        blank = True,
        null = True
    )
    message_context = JSONField(
        verbose_name = _(u'Message (Text)'),
        blank = True,
        null = True
    )
    subject_template = models.TextField(
        verbose_name = _(u'Template (Subject)'),
        blank = True,
        null = True
    )
    text_template = models.TextField(
        verbose_name = _(u'Template (Text)'),
        blank = True,
        null = True
    )
    html_template = models.TextField(
        verbose_name = _(u'Template (HTML)'),
        blank = True,
        null = True
    )
    when = models.IntegerField(
        verbose_name = _(u'When?'),
        choices = SEND_CHOICES,
        default = 0
    )
    keep = models.BooleanField(
        verbose_name = _(u'Keep?'),
        default = (not DELETE_AFTER_SEND),
        help_text = _(u'Enable to force-save the message')
    )
    is_sent = models.BooleanField(
        verbose_name = _(u'Is Sent?'),
        default = False
    )
    created_on = models.DateTimeField(
        verbose_name = _(u'Created on'),
        auto_now_add = True
    )

    def __unicode__(self):
        return "%s on %s" % (self.description, self.created_on)

    def save(self, *args, **kwargs):
        """
        Ensure that the message instance has been correctly defined before
        saving to the databse.
        """
        # Check if supplied templates exist before saving
        templates = [self.subject_template, self.text_template, self.html_template]
        for template in templates:
            if template:
                # If a template has been specified, ensure it exists
                try:
                    loader.get_template(template)
                except TemplateDoesNotExist:
                    raise ValidationError(_(u'Template does not exist: %s') % \
                        template)

        recipients = self.recipients

        # Ensure the recipients list is a list type
        if not type(recipients).__name__ == 'list':
            raise ValidationError(_(u'Recipients must be a list.'))

        # Ensure there is at least one recipient
        if not len(recipients):
            raise ValidationError(_(u'At least one recipient must be provided.'))

        # Allow the message instance to save
        super(MailifyMessage, self).save(*args, **kwargs)


    def send(self):
        """
        Sends the e-mail message. Will combine context variables with templates.
        """
        # Skip if the message has already been sent
        if self.is_sent:
            return True

        # Set the message subject
        if self.subject_context:
            if self.subject_template:
                subject = render_to_string(self.subject_template, \
                    self.subject_context)
            else:
                subject = render_to_string(DEFAULT_SUBJECT_TEMPLATE, \
                    self.subject_context)
        else:
            subject = ''

        # Set the message body
        if self.message_context:
            if self.text_template:
                text = render_to_string(self.text_template, \
                    self.message_context)
            else:
                text = render_to_string(DEFAULT_TEXT_TEMPLATE, \
                    self.message_context)

            if self.html_template:
                html = render_to_string(self.html_template, \
                    self.message_context)
            else:
                html = render_to_string(DEFAULT_HTML_TEMPLATE, \
                    self.message_context)
        else:
            text = ''
            html = ''

        # Send the message
        #for recipient in self.recipients:
        msg = Mailer(subject, text, self.sender, [force_unicode(r) for r in \
            self.recipients])
        msg.attach_alternative(html, 'text/html')
        msg.send()

        # Post-send handling
        self.is_sent = True
        self.save()
        if not self.keep:
            self.delete()