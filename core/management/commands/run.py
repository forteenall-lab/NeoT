from random import randint
from django.core.management.base import BaseCommand, CommandParser
from account.models import Accounts
from insta.bot import InstaBot
from orders.models import Orders, OrderStatus
from log.models import Logs
from time import sleep
from instagrapi import Client



class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('--order', type=int)
        parser.add_argument('--bot', type=int)
    
    def handle(self, *args, **options):
        print("set data done")
        # get args
        orderID = options["order"]
        botID = options["bot"]
        
        # find order and bot
        order = Orders.objects.get(pk=orderID, status=OrderStatus.ENEBALE)
        bot = order.bots.get(pk=botID)
        
        # create client
        client = Client()
        print("data founded. start login")
        
        
        try:
            client.login(bot.username, bot.password)
            Logs.objects.create(
                bot=bot,
                desc=f"ورود به حساب کاربری ربات با موفقیت انجام شد",
            )
            print(f"{bot.name} login success ✅")
        except Exception as e:
            print(f"{bot.name} login error")
            Logs.objects.create(
                bot=bot,
                desc=f"خطا در ورود به حساب کاربری \n{str(e)}",
            )
            bot.active = False
            bot.save()
            return None
            
        # find targeted medias
        target = client.user_id_from_username(order.campaignID)
        targetMedias = client.usertag_medias(target, 0)
        doActionCount = randint(bot.actionMin, bot.actionMax)
        # start action
        for media in targetMedias:
            try:
                
                # await for watch
                sleep(int(randint(bot.watchMin, bot.watchMax)/5))
                # do action
                # check for is post liked
                if media.has_liked:
                    continue
                
                # like the tag
                client.media_like(media.id)
                Logs.objects.create(
                    bot=bot,
                    order=order,
                    desc=f"لایک پست انجام شد {media.user.username} - {media.id}",
                )
                # await for watch
                sleep(int(randint(bot.watchMin, bot.watchMax)/2))
                # check for loops
                if doActionCount == bot.actionCount:
                    doActionCount += randint(bot.actionMin, bot.actionMax)
                    Logs.objects.create(
                        bot=bot,
                        order=order,
                        desc="اتمام عملیات لایک. شروع استراحت",
                    )
                    sleep(randint(bot.delayMin, bot.delayMax))
                    
            except Exception as e:
                print("error :(")
                print(e)
                bot.active = False
                bot.save()
                Logs.objects.create(
                    bot=bot,
                    order=order,
                    desc=f"خطا در انجام عملیات :(\n{str(e)}",
                )
                sleep(3600)
