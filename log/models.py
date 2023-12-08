from django.db import models



class Logs(models.Model):
    created_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ انجام اکشن",)
    bot = models.ForeignKey(
        "account.Accounts", 
        verbose_name="ربات انجام دهنده",
        on_delete=models.CASCADE,                    
        help_text="""
        انجام شده توسط""",
        editable=False
    )
    order = models.ForeignKey(
        "orders.Orders",
        verbose_name="سفارش مبدا",
        on_delete=models.CASCADE,
        help_text="""
        سفارشی که این ربات بر روی آن فعال شده است""",
        editable=False,
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        "account.Groups",
        verbose_name="گروه ربات",
        on_delete=models.CASCADE,
        help_text="""
        گروهی که ربات بر روی آن قرار دارد""",
        editable=False,
        null=True,
        blank=True
    )
    
    desc = models.TextField(
        verbose_name="توضیحات",
        null=True,
        blank=True,
        editable=False,
        max_length=2000,
    )
    
    def __str__(self):
        return f"{self.bot} -> {self.order}"

    class Meta:
        verbose_name_plural = "گزارشات"