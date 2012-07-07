from django.conf import settings


DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
DELETE_AFTER_SEND = getattr(settings, 'MAILIFY_DELETE_AFTER_SEND', True)
DEFAULT_DESCRIPTION = getattr(settings, 'MAILIFY_DEFAULT_DESCRIPTION', \
    'Message')
DEFAULT_SUBJECT_TEMPLATE = getattr(settings, \
    'MAILIFY_DEFAULT_SUBJECT_TEMPLATE', 'mailify/subject.txt')
DEFAULT_TEXT_TEMPLATE = getattr(settings, 'MAILIFY_DEFAULT_TEXT_TEMPLATE', \
    'mailify/message.txt')
DEFAULT_HTML_TEMPLATE = getattr(settings, 'MAILIFY_DEFAULT_HTML_TEMPLATE', \
    'mailify/message.html')

DEFAULT_WHEN = getattr(settings, 'MAILIFY_DEFAULT_WHEN', 0)
USE_CELERY = getattr(settings, 'MAILIFY_DEFAULT_CELERY', False)

if 'sendgrid' in settings.INSTALLED_APPS:
    USE_SENDGRID = getattr(settings, 'MAILIFY_USE_SENDGRID', True)
    if USE_SENDGRID:
        from sendgrid.message import SendGridEmailMultiAlternatives as Mailer
    else:
        from django.core.mail import EmailMultiAlternatives as Mailer
else:
    from django.core.mail import EmailMultiAlternatives as Mailer