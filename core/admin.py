from django.contrib import admin
from account.models import Accounts
from orders.models import Orders
from log.models import Logs


@admin.register(Accounts)
class AccountPanel(admin.ModelAdmin):
    list_display = ["pk", "name", "username", "active"]
    
    fieldsets = [
        (
            "اطلاعات اکانت",
            {
                "fields":[
                    "name",
                    "username",
                    "password",
                    "active"
                ]
            },
        ),
        (
            "تنظیمات",
            {
                "fields":[
                    "watchMin",
                    "watchMax",
                    "delayMin",
                    "delayMax",
                    "actionMin",
                    "actionMax",
                ]
            },
        ),
    ]
    

@admin.register(Orders)
class OrderPanel(admin.ModelAdmin):
    list_display = ["pk", "name", "status"]
    filter_horizontal = ["bots"]

@admin.register(Logs)
class LogsPanel(admin.ModelAdmin):
    list_display = ["bot", "_order", "created_at", "desc"]
    list_filter = ["order"]
    def _order(self, obj):
         return obj.order
    _order.empty_value_display = "سیستم"