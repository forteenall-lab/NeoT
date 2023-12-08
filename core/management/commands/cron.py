from django.core.management.base import BaseCommand
from account.models import Accounts
from insta.bot import InstaBot
from time import sleep

class test:
    def __init__(self, d) -> None:
        self.num = d
    
    def add(self):
        self.add += 1

bots = []

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        bots:list[InstaBot] = []
        
        while True:
            self.stdout.write(self.style.HTTP_INFO("start found bots"))
            
            # set all bot into list
            for account in Accounts.objects.exclude(username__in=[tmp.account.username for tmp in bots]):
                self.stdout.write(self.style.SUCCESS("found account setup it"))
                bots.append(InstaBot(account))
        
            for bot in bots:
                # check start work
                if bot.onWork or not bot.account.active:
                    continue
                            
                bot.start()
            sleep(5)