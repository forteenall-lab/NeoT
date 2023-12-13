from django.core.management.base import BaseCommand
from account.models import Accounts
from insta.bot import InstaBot
import asyncio
from asgiref.sync import sync_to_async




async def main():
    bots:dict[str, InstaBot] = {}
    
    while True:
        print("check for installed bots")        
        # set all bot into list
        async for account in Accounts.objects.all():
            if not account.active or account.name in list(bots.keys()):
                continue
            
            bots[account.name] = InstaBot(account)
            asyncio.create_task(bots[account.name].start())
    
        await asyncio.sleep(60)

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print("NeoT start Working\nhappy hacking:)")
        asyncio.run(main())