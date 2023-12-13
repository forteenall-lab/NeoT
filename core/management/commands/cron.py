from django.core.management.base import BaseCommand
from account.models import Accounts
from insta.bot import InstaBot
from orders.models import OrderStatus, Orders
from subprocess import Popen




class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print("NeoT start Working\nhappy hacking:)")
        
        for order in Orders.objects.filter(status=OrderStatus.ENEBALE):
            for bot in order.bots.filter(active=True):
                print(f"start shell for order: {order.pk} bot: {bot.pk}")
                Popen([f"python manage.py run --order {order.pk} --bot {bot.pk}"], shell=True)