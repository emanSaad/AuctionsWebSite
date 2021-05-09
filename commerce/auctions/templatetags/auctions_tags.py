from django import template
from ..models import WatchList, Auction

register = template.Library()

"""
This custom tag allows the user to see the number of items in his watch list 
in the navbar of the site. meaning that this tag will be available for all HTML template.

"""          
@register.simple_tag(takes_context=True)
def total_items_in_watchlist(context):
    request = context['request']

    watchlist = WatchList.objects.filter(user=request.user) 
    total_items = watchlist.count()
    return total_items
