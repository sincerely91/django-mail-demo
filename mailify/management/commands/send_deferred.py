from optparse import make_option

from django.core.management.base import BaseCommand

from mailify.models import MailifyMessage
from mailify.tasks import task_send_mail


class Command(BaseCommand):
    option_list = BaseCommand.option_list
    option_list += (
        make_option('-c', '--celery', action='store_true', dest='use_celery',
            default=False, help="Use celery to process deferred messages."
        ),
    )
    help = "Send deferred and unsent mail."

    def handle(self, *args, **options):
        messages = MailifyMessage.objects.filter(is_sent=False)
        if options['use_celery']:
            print "Sending %d messages with Celery..." % len(messages)
        else:
            print "Sending %d messages..." % len(messages)

        for message in messages:
            if options['use_celery']:
                task_send_mail.delay(message)
            else:
                message.send()
        print "Done!"