from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from account.models import Accounts

class Command(BaseCommand):
    def add_arguments(self, parser):
        # get app name
        parser.add_argument("bot", type=str)

    def handle(self, *args, **options):
        botID = options["bot"]
        
        bot = Accounts.objects.get(pk=botID)