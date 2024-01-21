from time import sleep
from django.core.management.base import BaseCommand
from pydantic import conset
from account.models import Accounts
from insta.bot import InstaBot
from orders.models import OrderStatus, Orders
from subprocess import Popen




class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print("NeoT start Working\nhappy hacking:)")
        

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        orders = []
        bots = []
        
        while True:
            print(f"check for installed bots -- active bots: {bots}")
            
            # set orders in project
            for order in Orders.objects.exclude(pk__in=orders, status=OrderStatus.DISABLE):
                for bot in order.bots.filter(active=True):
                    
                    if bot.pk in bots:
                        continue
                    
                    print(f"start shell for order: {order.pk} bot: {bot.pk}")
                    Popen([f"python3 manage.py run --order {order.pk} --bot {bot.pk}"], shell=True)
                    bots.append(bot.pk)
                orders.append(order.pk)
            sleep(60)