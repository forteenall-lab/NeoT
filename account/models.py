from django.db import models



class Accounts(models.Model):

    name = models.CharField(
        "نام ربات", 
        max_length=50,
        help_text="""
        این نام ربات در نام اکانت قرار خواهد گرفت"""
    )

    username = models.CharField(
        "نام کاربری ربات", 
        max_length=100,
        help_text="""
        نام کاربری ربات در اینیستا گرام"""
    )
    
    password = models.CharField(
        "رمزعبور ربات", 
        max_length=100,
        help_text="""
        رمزعبور اکانت ربات در اینیستاگرام"""
    )
    
    
    active = models.BooleanField(
        "فعال",
        default=True,
        help_text="""
        در صورت غیر فعال بودن این گزینه ربات کار نخواهد کرد"""
    )
    
    watchMin = models.IntegerField(
        "حداقل مشاهده پست (ثانیه)",
        default=20,
        help_text="""
        عدد رندوم مشاهده پست ربات از این مقدار بیشتر خواهد بود"""
    )
    
    watchMax = models.IntegerField(
        "حداکثر مشاهده پست (ثانیه)",
        default=50,
        help_text="""
        عدد رندوم مشاهده پست ربات از این مقدار کمتر خواهد بود"""
    )

    delayMin = models.IntegerField(
        "حداقل استراحت (دقیقه)",
        default=10,
        help_text="""
        عدد رندوم استراحت ربات از این مقدار بیشتر خواهد بود"""
    )
    
    delayMax = models.IntegerField(
        "حداکثر استراحت (دقیقه)",
        default=40,
        help_text="""
        عدد رندوم استراحت ربات از این مقدار کمتر خواهد بود"""
    )
    
    actionMin = models.IntegerField(
        "حداقل اکشن",
        default=10,
        help_text="""
        عدد رندوم اکشن ربات از این مقدار بیشتر خواهد بود"""
    )
    
    actionMax = models.IntegerField(
        "حداکثر اکشن",
        default=40,
        help_text="""
        عدد رندوم اکشن ربات از این مقدار کمتر خواهد بود"""
    )
    
    actionCount = models.IntegerField(
        "تعداد عملیات",
        default=10,
        help_text="""
        تعداد عملیاتی که این ربات تا بحال انجام داده است"""
    )
    
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "ربات ها"