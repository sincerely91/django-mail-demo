==============
django-mailify
==============

Enhance the builtin Django mail functionality to include task queueing

Getting Started
---------------

# Install django-mailify
    pip install -e git://github.com/keithio/django-mailify.git#egg=mailify

# Add ``mailify`` to your ``INSTALLED_APPS``
    INSTALLED_APPS += (
        'mailify',
    )

Configuration
-------------

``DEFAULT_FROM_EMAIL``: your default sender e-mail address, can use with or without name
    DEFAULT_FROM_EMAIL = 'Admin <admin@example.com>'