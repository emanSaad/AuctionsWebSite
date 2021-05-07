from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.generic.base import TemplateView
from django.db.models import Max
from django.core.mail import send_mail
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views.generic import ListView

from .models import User, Auction, Category,Bid, WatchList
from .forms import AuctionForm, CommentForm, BidForm, EmailLisingForm


def index(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    listings = Auction.objects.filter(status='active')

    # if the user choose a category, list the listings og this category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        listings = listings.filter(category=category)
    return render(request,"auctions/index.html",{
        'listings': listings,
        'category': category,
        'categories': categories
    })

# # using class based view
# class AuctionListView(ListView):
#     queryset = Auction.objects.all()

#     # the context variable for the queryset results
#     context_object_name = 'listings'

#     # number of listingd per page
#     paginate_by = 3
#     template_name = "auctions/index.html"

# share Listing view
def share_listing(request, listing_id):
    # retreive listing by id
    listing = get_object_or_404(Auction, id=listing_id, status='active')
    sent = False
    if request.method == "POST":
        form = EmailLisingForm(request.POST)
        if form.is_valid():
            cleanData = form.cleaned_data
            # send email
            # get the url of the listing, because we need to include the listing link in the sent email
            listing_url = request.build_absolute_uri(listing.get_absolute_url())
            subject = f"{cleanData['name']} recommends you see " \
                      f"{listing.item_name}"
            message = f"See {listing.item_name} at {listing_url}\n\n" \
                      f"{cleanData['name']}\'s comments: {cleanData['comments']}"
            send_mail(subject, message, 'em.alhaweri@gmail.com', [cleanData['to']])
            sent = True
    else:
        form = EmailLisingForm()
    return render(request,"auctions/share_listing.html",{
        'listing': listing,
        'form': form,
        'sent':sent
    })    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    """
    Create a new auction listing.
    """
    categories = Category.objects.all().values('name')
    if request.method == "POST":
    
        category = Category.objects.get(id=1)
        # category = get_object_or_404(Auction, id=1)
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            item_name = form.cleaned_data["item_name"]
            description = form.cleaned_data["description"]
            close_date = form.cleaned_data["close_date"]
            base_price = form.cleaned_data["base_price"]
            status = form.cleaned_data["status"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data['category']
            instance = form.save(commit=False)
            
            # category = AuctionForm(instance=category)
            # instance.category = form.request.POST.get['category']
            # instance.category = category
            # to get the user instance from the User model, This gives the logged in user 
            form.instance.user = request.user
            instance.save()
            img_obj = form.instance
            return render(request, "auctions/create_listing.html",{
                'form': form,
                'img_obj': img_obj,
                'categories': categories
            })
        else:
            return render(request, "auctions/create_listing.html",{
                'form': form,
                'categories': categories
            })
            
    return render(request, "auctions/create_listing.html",{
        'form': AuctionForm(),
        'categories': categories
    })

def auction_listings(request):
    pass
    
    # listings = Auction.objects.filter(status=0).order_by('-posting_date')
    # return render(request, "auctions/auction_listings.html",{
    #     'listings': listings  
    # })

def _get_form(request, formName, prefix):
    data = request.POST if prefix in request.POST else None
    return formName(data, prefix=prefix)


class listing_details(TemplateView):
    template_name = 'auctions/listing_details.html'
    now = timezone.now()

    def get_model_objects(self, request,*args, **kwargs):
        auction_is_closed = False
        # get the current listing
        listing = get_object_or_404(Auction, item_name= kwargs['item_name'])

        # Get the close datte/time for the auction
        close_date = listing.close_date
        print("close date: ",close_date)
        
        # check if time passes the close date, return false
        if self.now > close_date:
            auction_is_closed = True

        # retrieve all active related comments to this listing 
        comments = listing.comments.filter(active=True)
        
        #retreive all bids that have been done on this listing
        bids = listing.bids.all()
        if not bids:
            last_bid = None
        else:
            last_bid = bids.latest('price')
                 
        return listing, comments, last_bid, bids, close_date, auction_is_closed


    def get(self, request, *args, **kwargs):        
        [listing, comments, last_bid, bids, close_date, auction_is_closed] = self.get_model_objects(self, request, *args, **kwargs) 

        # if the user is the one who create the listing, allows him to edit or delete this listing
        edit_permission = True
        if request.user == listing.user:
            edit_permission = False

        return self.render_to_response({
            'bid_form': BidForm(prefix='bidformsub'),
            'comment_form': CommentForm(prefix='commentformsub'),
            'listing': listing,
            'comments': comments,
            'bids': bids,
            'last_bid': last_bid,
            'auction_is_closed': auction_is_closed,
            'edit_permission': edit_permission
        })

    # when posting data from user
    def post(self, request, *args, **kwargs):
        [listing, comments, last_bid, bids, close_date, auction_is_closed] = self.get_model_objects(self, request, *args, **kwargs)
        new_comment = None
        new_bid = None
        bid_form = _get_form(request, BidForm, 'bidformsub')
        comment_form = _get_form(request, CommentForm, 'commentformsub')

        # get the base price of listing
        base_price = listing.base_price
        
        if bid_form.is_bound and bid_form.is_valid():
            new_bid = bid_form.save(commit=False)
            bid_form.instance.user_name = request.user
            new_bid.listing = listing

            """
            Check if there are already bids or not,
            if None compare the new bid with base price
            if there are already bids, retrieve the max bid and compare it to the new bid. 
            """
            all_bids = Bid.objects.all().values('price')
            print("all Bids price", all_bids)
            if all_bids == None or last_bid == None: 
                
                if new_bid.price < base_price:
                    return HttpResponse('<h2>The bid should be at least as the base price, please put another bid</h2>')
                else:
                    new_bid.save()
                    last_bid = new_bid
            else:
                
                last_bid = bids.latest('price')
                if new_bid.price <= last_bid.price:
                    return HttpResponse('<h2>The bid should be at least as the last bid, please put another bid</h2>')
                else:
                    new_bid.save()
                    last_bid = new_bid
        
        # Now process the comment form
        elif comment_form.is_bound and comment_form.is_valid():
            new_comment = comment_form.save(commit=False)

            # Assign the user who put the comment
            comment_form.instance.user_name = request.user

            # assign the current listing to the comment
            new_comment.listing = listing
            new_comment.save()
        
        return render(request, self.template_name,{
            'listing': listing,
            'comments': comments,
            'bids': bids,
            'last_bid': last_bid, 
            'bid_form': bid_form,
            'comment_form': comment_form,
            'new_comment': new_comment,
            'bid_form': bid_form,
            'auction_is_closed': auction_is_closed

        })

def add_to_watchlist(request, listing_id ):
    item = get_object_or_404(Auction, pk=listing_id)
    
    #get the watchlist items of this user
    user_listings = WatchList.objects.filter(user=request.user)
    
    if request.method == "POST":
        user_listing, created = WatchList.objects.get_or_create(user=request.user, watchlist = item)
        print("user_listing: ", user_listing)
        
        if not created:
            message = "This listing is already exist in your watchlist."
        else:
            message = "Your listing has been added."

        return render(request, "auctions/add_to_watchlist.html",{
                
            'message': message,
            'created': created,
            'user_listings': user_listings,
            'created': created
        })
    return render(request, "auctions/listing_details.html")


""" get all watchlist items for current user """
def watchlist_items(request):
    listings = WatchList.objects.filter(user=request.user)
    print("listings in watchList:", listings)
    # listings = listings.values_list()
    print("watchlist listings: ", listings) 
    return render(request, "auctions/watchlist_items.html", {
        'listings': listings
    })


def delete_listing(request, listing_id):
    
    if request.method == "POST":
        # get the selected item by user, then delete it from this user watchlist
        listing = WatchList.objects.get(pk=listing_id)
        listing.delete()
        user_listings = WatchList.objects.filter(user=request.user)
        
        
        return render(request, "auctions/add_to_watchlist.html",{
            'user_listings': user_listings
        })
    return render(request, "auctions/add_to_watchlist.html")


# This for user to edit the auction who created  
def edit_listing(request, listing_id):

    listing = get_object_or_404(Auction, pk=listing_id)
    print("This listing:", listing)
    # we need listings and category when we redirect the user to the index.html
    listings = Auction.objects.all()
    category = Category.objects.filter(id=1)
    
    categories = Category.objects.all().values('name')    
    form = AuctionForm(request.POST or None, request.FILES, instance=listing)
    if form.is_valid():
        form.save()
        
        # print("form_IsValid:", form.is_valid())
        # print("cleaned Data: ", form.cleaned_data)
            
        return render(request, "auctions/index.html",{ 
            "categories": categories,
            "listings": listings,
            "category": category,
        })
    
    form = AuctionForm(instance=listing)  
    return render(request,"auctions/edit_listing.html",{
        "form": form,
        "categories": categories,
        "listing": listing
        
    })
    
