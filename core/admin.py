from django.contrib import admin
from account.models import Accounts, Groups
from orders.models import Orders
from log.models import Logs

@admin.register(Groups)
class GroupsPanel(admin.ModelAdmin):
    list_display = ["pk", "name"]

@admin.register(Accounts)
class AccountPanel(admin.ModelAdmin):
    list_display = ["pk", "name", "username", "active"]
    filter_vertical = ["group"]
    
    fieldsets = [
        (
            "اطلاعات اکانت",
            {
                "fields":[
                    "name",
                    "username",
                    "password",
                    "group",
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
    list_display = ["pk", "name", "group", "status", "start", "end"]

@admin.register(Logs)
class OrderPanel(admin.ModelAdmin):
    list_display = ["bot", "group", "order", "created_at", "desc"]