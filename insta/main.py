from account.models import Accounts
from log.models import Logs
from orders.models import Orders
from instagrapi import Client
from random import randint
from time import sleep


class InstaBot:
    
    def __init__(self, account:Accounts):
        self.account = account
        self.client = Client()
        self.client.login(self.account.username, self.account.password)
        self.target = None

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

    @property
    def botOrders(self):
        """get bot orders"""
        return Orders.objects.filter(group_id=self.account.group.all().values_list("pk", falt=True))

    def doAction(self, media, order):
        """do an action"""
        # check for is post liked
        if media.has_liked:
            return False
        
        # like the tag
        self.client.media_like(media.id)                
        sleep(self.watchDelay)
        
        self.logAction(
            order=order,
            desc="لایک پست انجام شد"
        )
        
        # add number in database   
        self.account.actionCount += 1
        self.account.save()
        
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
    
    def logAction(self, order:Orders, desc:str):
        """log what's bot do"""
        
        log = Logs(
            bot=self.account,
            order=order,
            group=order.group,
            desc=desc,
        )
        log.save()

    def start(self):
        orders = self.botOrders
        IDs = []
        for order in orders:
            # check for exsits
            if order.campaignID in IDs:
                continue
            IDs.append(order.campaignID)
            
            # set bot on page
            self.setBotOnPage(order.campaignID)
            
            # start action
            for i, media in enumerate(self.targetMedias):
                try:
                    
                    # do action
                    if not self.doAction(media, order):
                        continue
                    
                    # check for loops
                    if doActionCount == self.account.actionCount:
                        doActionCount += self.doActionCount 
                        self.logAction(order=order, desc="اتمام عملیات لایک. شروع استراحت")
                        sleep(self.restDelay)
                        
                except Exception as e:
                    print("error :(")
                    print(e)
                    
                    sleep(3600)

            sleep(self.restDelay*10)