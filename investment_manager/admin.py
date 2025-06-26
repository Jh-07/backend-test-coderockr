from django.contrib import admin

from investment_manager.models import Owner, Investment


class Owners(admin.ModelAdmin):
    list_display = ('id', 'name', 'birthday')
    list_display_links = ('id','name')
    list_per_page = 20
    search_fields = ('nome', 'age')

admin.site.register(Owner,Owners)

class Investments(admin.ModelAdmin):
    list_display = ('id', 'owner', 'amount', 'creation_date', 'withdraw_date')
    list_display_links = ('id','owner')
    list_per_page = 20
    search_fields = ('owner', 'amount')

admin.site.register(Investment, Investments)