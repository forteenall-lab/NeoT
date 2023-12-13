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
        print(f"bot {self.account.username} started ...")
        