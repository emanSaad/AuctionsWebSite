from django.contrib import admin

from .models import User, Auction, Bids, Comments

# Register your models here.

admin.site.register(User)

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['user','item_name', 'posting_date', 'close_date', 'base_price', 'status']
    list_editable = ['item_name', 'close_date', 'base_price', 'status']

@admin.register(Bids)
class BidsAdmin(admin.ModelAdmin):
    list_display = ['item' , 'price', 'time', 'number_of_bids']

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'listing', 'created_on', 'content', 'active']
    list_editable = ['content', 'active']
