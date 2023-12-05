from django.db import models



class OrderStatus(models.IntegerChoices):
    ENEBALE = 0, "فعال"
    DISABLE = 1, "غیر فعال"
    

class Orders(models.Model):
    
    name = models.CharField(
        "نام سفارش",
        max_length=100,
        help_text="""
        این گزینه صرفا جنبه نمایشی دارد"""
    )

    campaignID = models.CharField(
        "آیدی کمپین",
        max_length=100,
        help_text="""
        آیدی کمپین برای انجام عملیات
        ربات بر روی گزینه تگ های این کمپین
        اکشن انجام خواهد داد"""
    )

    group = models.ForeignKey(
        "account.Groups",
        verbose_name="گروه عامل",
        on_delete=models.CASCADE,
        help_text="""
        این سفارش توسط گروه تعیین شده انجام
        خواهد شد"""
    )
    
    status = models.IntegerField(
        "وضعیت انجام",
        choices=OrderStatus.choices,
        default=OrderStatus.ENEBALE,
        help_text="""
        وضعیت انجام سفارش تعیین کننده فعالیت گروه است
        در صورت انتظار بودن این گزینه ربات های گروه این مورد را
        انجام خواهند داد. در غیر اینصورت انجام نخواهد شد"""
    )
    
    
    start = models.TimeField(
        "ساعت شروع گروه", 
        help_text="""
        در این زمان گروه ربات ها شروع به فعالیت خواهند کرد"""
    )
    
    end = models.TimeField(
        "ساعت پایان گروه", 
        help_text="""
        در این زمان گروه ربات ها به فعالیت خود پایان خواهند داد"""
    )
    class Meta:
        verbose_name_plural = "کمپین ها"

    def __str__(self):
        return self.name
