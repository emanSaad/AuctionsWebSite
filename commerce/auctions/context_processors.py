from .models import Auction

# custom context processors
def get_listing(request):
    listing = Auction.objects.latest('-id')
    return {'listing': listing }