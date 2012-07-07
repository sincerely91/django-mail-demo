==============
django-mailify
==============

Enhance the builtin Django mail functionality to include task queueing or deferment.

Why another mail app?
---------------------

Djano mailer seems to be quite popular, but I wanted to take advantage of Celery workers rather 
than depend on a lock file that has unpredictable behavior on various hosts. Additionally, I wanted
the option to use the same interface to save some messages to send later via a cron job.

Another benefit of ``django-mailify`` is that each message can make use of its own template complete
with their own context. So, if you want a certain e-mail type to have one template made by a designer,
you can reference that one, while others may have a different format. The combination of the template
with the context happens at the time you ``send``, so that processing power can be done via Celery or 
at a non-peak moment, or immediately if so desired.

Getting Started
---------------

0. Requirements::

    Django>=1.4
    South>=0.7.5
    jsonfield>=0.9

1. Install django-mailify::

    pip install -e git://github.com/keithio/django-mailify.git#egg=mailify

2. Add ``mailify`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS += (
        'mailify',
    )

Configuration
-------------

All of the following are optional, but highly recommended.

``DEFAULT_FROM_EMAIL``: your default sender e-mail address, can use with or without name::

    DEFAULT_FROM_EMAIL = 'Admin <admin@example.com>'

``MAILIFY_DELETE_AFTER_SEND``: whether or not to delete the message from the database after successful send (default=True)::

    MAILIFY_DELETE_AFTER_SEND`` = True

``MAILIFY_DEFAULT_DESCRIPTION``: a description of the e-mail message, for internal use only (default='Message')::

    MAILIFY_DEFAULT_DESCRIPTION = 'MySite Correspondence'

``MAILIFY_DEFAULT_SUBJECT_TEMPLATE``: the subject template to be used by default (default='mailify/subject.txt')::

    MAILIFY_DEFAULT_SUBJECT_TEMPLATE = 'mysite/templates/messages/subject.txt'

``MAILIFY_DEFAULT_TEXT_TEMPLATE``: the plaintext message template to be used by default (default='mailify/message.txt')::

    MAILIFY_DEFAULT_TEXT_TEMPLATE = 'mysite/templates/messages/message.txt'

``MAILIFY_DEFAULT_HTML_TEMPLATE``: the HTML message template to be used by default (default='mailify/message.html')::

    MAILIFY_DEFAULT_HTML_TEMPLATE = 'mysite/templates/messages/message.html'

``MAILIFY_DEFAULT_WHEN``: when to send the message, 0 - now, 1 - delay with celery, 2 - defer (default=0)::

    MAILIFY_DEFAULT_WHEN = 0  # Send the message now
    MAILIFY_DEFAULT_WHEN = 1  # Utilize task queueing from Celery
    MAILIFY_DEFAULT_WHEN = 2  # Defer until later, process queue with send_deferred management command

``MAILIFY_USE_CELERY``: whether or not to use Celery when creating a message, for use with ``message`` signal (default=False)::

    MAILIFY_USE_CELERY = True

Using Celery
------------

Ensure that you have Celery installed ``django-celery`` and have added ``'kombu.transport.django'`` and ``djcelery`` to your `INSTALLED_APPS`` before ``mailify``.

Then, simply use the correct triggers and settings variables to ensure proper assignment to your worker(s).

Usage
-----

1. Using signals::

    from mailify.signals import message

    message.send([parameters])

    """
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
    """

2. Using model instantiation::

    from mailify.models import MailifyMessage

    new_message = MailifyMessage(...)

    # Check models.py for reference.

Future Work
-----------

* Integrate support for django-sendgrid_

.. _django-sendgrid: https://github.com/RyanBalfanz/django-sendgrid

