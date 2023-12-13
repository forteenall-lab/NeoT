from account.models import Accounts
from log.models import Logs
from orders.models import Orders, OrderStatus
from instagrapi import Client
from random import randint
import asyncio
from asgiref.sync import sync_to_async


class InstaBot:
    
    def __init__(self, account:Accounts):
        self.account = account
        self.client = Client()
        self.target = None
        self.onWork = False
        print(f"create bot {self.account.username} done.")
        
        
        return None

    @property
    def watchDelay(self):
        """how many time watch the post?"""
        return randint(self.account.watchMin, self.account.watchMax)        
    
    @property
    def restDelay(self):
        """delay between bucket"""
        return randint(self.account.delayMin, self.account.delayMax)
    
    @property
    def doActionCount(self):
        """action count do in each work time"""
        return randint(self.account.actionMin, self.account.actionMax)
    
    @property
    def targetMedias(self):
        """
        get media in target
        
        Args:
            count (number): count of medias in client
        """
        if self.target is None:
            raise Exception("target is invalid\nrun setBotOnPage function")
        
        return self.client.usertag_medias(self.target, self.mediaCount)



    def doAction(self, media, order):
        """do an action"""
        # check for is post liked
        if media.has_liked:
            return False
        
        # like the tag
        self.client.media_like(media.id)
        return True
    
    def setBotOnPage(self, ID:str, mediaCount:int=0):
        """
        set bot on campaign page
        after bot go to campaign tagged section

        Args:
            ID (string): campaign target ID
            mediaCount (number): media bot worked
                                 default == all
        """
        self.target = self.client.user_id_from_username(ID)
        self.mediaCount = mediaCount
    
    
    async def start(self):
        """
        this function get all target of group
        that equle with bot group
        get bot posts and do action in posts
        """
        try:
            self.client.login(self.account.username, self.account.password)
            await Logs.objects.acreate(
                bot=self.account,
                desc=f"ورود به حساب کاربری ربات {self.account.username} با موفقیت انجام شد",
            )
            print(f"{self.account.name} login success ✅")
        except Exception as e:
            await Logs.objects.acreate(
                bot=self.account,
                desc=f"خطا در ورود به حساب کاربری  {self.account.username}",
            )
            self.account.active = False
            self.account.save()
            print(f"{self.account.name} login error")
            
        self.onWork = False
        tmp_groupid = []
        # get groups of bot
        async for group in self.account.group.all():
            tmp_groupid.append(group.pk)
        IDs = []
        # start action
        async for order in Orders.objects.filter(group_id__in=tmp_groupid, status=OrderStatus.ENEBALE):
            # check for exsits
            if order.campaignID in IDs:
                continue
            IDs.append(order.campaignID)
            
            # set bot on page
            self.setBotOnPage(order.campaignID)
            
            # start action
            for i, media in enumerate(self.targetMedias):
                try:
                    
                    # await for watch
                    await asyncio.sleep(int(self.watchDelay/2))
                    # do action
                    if not self.doAction(media, order):
                        continue
                    Logs.objects.acreate(
                        bot=self.account,
                        order=order,
                        group=order.group,
                        desc=f"لایک پست انجام شد {media.user.username} - {media.id}",
                    )
                    # await for watch
                    await asyncio.sleep(int(self.watchDelay/2))
                    # check for loops
                    if doActionCount == self.account.actionCount:
                        doActionCount += self.doActionCount 
                        Logs.objects.acreate(
                            bot=self.account,
                            order=order,
                            group=order.group,
                            desc="اتمام عملیات لایک. شروع استراحت",
                        )
                        await asyncio.sleep(self.restDelay)
                        
                except Exception as e:
                    print("error :(")
                    print(e)
                    self.account.active = False
                    await sync_to_async(self.account.save)()
                    Logs.objects.acreate(
                        bot=self.account,
                        order=order,
                        group=order.group,
                        desc=f"خطا در انجام عملیات {self.account.username} :(",
                    )
                    await asyncio.sleep(3600)

            await asyncio.sleep(self.restDelay*10)
        self.onWork = False