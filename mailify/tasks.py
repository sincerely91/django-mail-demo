
from celery.task import task

@task
def task_save_message(message):
    """
    Use celery to create a message.
    """
    message.save()

@task
def task_send_mail(instance):
    """
    Use celery to send a message.
    """
    instance.send()
