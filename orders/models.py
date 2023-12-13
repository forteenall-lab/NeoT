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

    bots = models.ManyToManyField(
        "account.Accounts",
        verbose_name="ربات های عامل",
        help_text="""
        این سفارش توسط ربات های تعیین شده انجام
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
    
    class Meta:
        verbose_name_plural = "کمپین ها"

    def __str__(self):
        return self.name
