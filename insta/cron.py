from account.models import Accounts
from insta.bot import InstaBot

bots:list[InstaBot] = [1, 2, 3, 5, 6]
def action():

    # set all bot into list        
    # for account in Accounts.objects.exclude(username__in=[tmp.account.username for tmp in bots]):
    #     bots.append(InstaBot(account))

    for bot in bots:
        # check start work
        # if bot.onWork:
        #     continue
        
        # bot.start()
        print(bot)
    