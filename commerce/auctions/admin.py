from django.contrib import admin

from .models import User, Category, Auction, Bid, Comments, WatchList

# Register your models here.

admin.site.register(User)

@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['user','item_name','slug', 'posting_date', 'close_date', 'base_price', 'status']
    list_editable = ['item_name', 'close_date', 'base_price', 'status']
    prepopulated_fields = {'slug': ('item_name',)}

@admin.register(Bid)
class BidsAdmin(admin.ModelAdmin):
    list_display = ['listing' , 'price', 'created_on']

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'listing', 'created_on', 'content', 'active']
    list_editable = ['content', 'active']
