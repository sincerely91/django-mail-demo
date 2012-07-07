from django.db.models.signals import post_save
from django.dispatch import receiver
from models import MailifyMessage
from settings import DELETE_AFTER_SEND, USE_CELERY
from signals import message
from tasks import task_save_message, task_send_mail


@receiver(message)
def handle_message(sender, **kwargs):
    """
    Handles the use of the message signal to create the message.

    Parameters::

        desc: string, description of the message, default='Message'
        frm: string, from address, default=settings.DEFAULT_FROM_EMAIL
        recipients: list, recipient e-mail addresses, required
        celery: boolean, whether to use celery to initialize the message, default=False
        when: 0 -- send message now (default)
              1 -- delay and process with celery
              2 -- defer and send later with management command
        keep: boolean, whether to keep the message in the database after sending, default=False
        subject_context: dict, key-value pairs for completing subject template
        message_context: dict, key-value pairs for completing message templates
        subject_template: string, template for subject
        text_template: string, template for text message
        html_template: string, template for HTML message

    Usage::

        from mailify.signals import message

        message.send(desc='...', recipients=[...], celery=True, when=2)
    """
    desc = kwargs.get('desc', None)
    frm = kwargs.get('from', None)
    recipients = kwargs.get('recipients', None)
    celery = kwargs.get('celery', USE_CELERY)
    when = kwargs.get('when', 0)
    keep = kwargs.get('keep', (not DELETE_AFTER_SEND))
    subject_context = kwargs.get('subject_context', None)
    message_context = kwargs.get('message_context', None)
    subject_template = kwargs.get('subject_template', None)
    text_template = kwargs.get('text_template', None)
    html_template = kwargs.get('html_template', None)

    new_message = MailifyMessage(
        description = desc,
        sender = frm,
        recipients = recipients,
        when = when,
        keep = keep,
        subject_context = subject_context,
        message_context = message_context,
        subject_template = subject_template,
        text_template = text_template,
        html_template = html_template
    )

    if celery:
        # Add the message creation to the task queue
        task_save_message.delay(new_message)
    else:
        # Save the message now
        new_message.save()


@receiver(post_save, sender=MailifyMessage)
def handle_post_save(sender, instance, *args, **kwargs):
    """
    Called after a MailifyMessage instance is created.

    Do not use in conjunction with ``message.send()`` signal.
    """
    if instance.when == 0:
        # NOW: send the message now
        instance.send()
    elif instance.when == 1:
        # DELAY: add the message to the task queue
        task_send_mail.delay(instance)
    else:
        # DEFER: message stays in the database, must be sent with a management
        #        command
        pass