from django import template
from ..models import WatchList, Auction

register = template.Library()
          
@register.simple_tag(takes_context=True)
def total_items_in_watchlist(context):
    request = context['request']

    watchlist = WatchList.objects.filter(user=request.user) 
    total_items = watchlist.count()
    return total_items
