from django.contrib import admin
from models import MailifyMessage


class MailifyMessageAdmin(admin.ModelAdmin):
    list_display = ('description', 'sender', 'recipients', 'when', 'is_sent', 'created_on')
    search_fields = ('description', 'text_message', 'html_message')
    list_filter = ('when', 'is_sent', 'created_on')

admin.site.register(MailifyMessage, MailifyMessageAdmin)