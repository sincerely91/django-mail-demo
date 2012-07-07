from django.dispatch import Signal


message = Signal(providing_args=['desc', 'from', 'recipients', 'celery', 'when',
    'keep', 'subject_context', 'message_context', 'subject_template',
    'text_template', 'html_template'])