==============
django-mailify
==============

Enhance the builtin Django mail functionality to include task queueing or deferment.

Getting Started
---------------

1. Install django-mailify::

    pip install -e git://github.com/keithio/django-mailify.git#egg=mailify

2. Add ``mailify`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS += (
        'mailify',
    )

Requirements::

    Django>=1.4
    South>=0.7.5
    jsonfield>=0.9

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