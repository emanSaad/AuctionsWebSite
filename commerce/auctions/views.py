from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.generic.base import TemplateView
from django.db.models import Max
import datetime
from .models import User, Auction, Category,Bid
from .forms import AuctionForm, CommentForm, BidForm





def index(request):
    listings = Auction.objects.all()
    return render(request, "auctions/index.html",{
        'listings': listings
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    """
    Create a new auction listing.
    """
    categories = Category.objects.all().values('name')
    if request.method == "POST":
        category = Category.objects.get(id=1)
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            item_name = form.cleaned_data["item_name"]
            description = form.cleaned_data["description"]
            close_date = form.cleaned_data["close_date"]
            base_price = form.cleaned_data["base_price"]
            status = form.cleaned_data["status"]
            image = form.cleaned_data["image"]

            instance = form.save(commit=False)
            instance.category = category
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
    
    listings = Auction.objects.filter(status=0).order_by('-posting_date')
    return render(request, "auctions/auction_listings.html",{
        'listings': listings  
    })

def _get_form(request, formName, prefix):
    data = request.POST if prefix in request.POST else None
    return formName(data, prefix=prefix)


class listing_details(TemplateView):
    template_name = 'auctions/listing_details.html'
    # now = datetime.datetime.now()
    now = timezone.now()

    

    def get_model_objects(self, request,*args, **kwargs):
        auction_is_closed = False
        # get the current listing
        listing = get_object_or_404(Auction, item_name= kwargs['item_name'])

        # Get the close datte/time for the auction
        close_date = listing.close_date
    
        # check if time passes the close date, return false
        if self.now > close_date:
            auction_is_closed = True
        # retrieve all active related comments to this listing 
        comments = listing.comments.filter(active=True)

        #retreive all bids that have been done on this listing
        bids = listing.bids.all()
        last_bid = bids.latest('price')
        # last_bid = Bid.objects.all().values('price').order_by('created_on')[:2]

        return listing, comments, bids, last_bid, close_date, auction_is_closed


    def get(self, request, *args, **kwargs):
                
        [listing, comments, bids, last_bid, close_date, auction_is_closed]=self.get_model_objects(self, request, *args, **kwargs) 
        return self.render_to_response({
            'bid_form': BidForm(prefix='bidformsub'),
            'comment_form': CommentForm(prefix='commentformsub'),
            'listing': listing,
            'comments': comments,
            'bids': bids,
            'last_bid': last_bid,
            'auction_is_closed': auction_is_closed
        })

    # when posting data from user
    def post(self, request, *args, **kwargs):
        [listing, comments, bids, last_bid, close_date, auction_is_closed] = self.get_model_objects(self, request, *args, **kwargs)
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
            if all_bids == None: 
                if new_bid.price < base_price:
                    return HttpResponse('<h2>The bid should be at least as the base price, please put another bid</h2>')
                else:
                    new_bid.save()
                    return render(request, self.template_name,{
                    'listing': listing,
                    'bid_form': bid_form,
                    'bids': bids,
                    'new_bid': new_bid,
                    'last_bid': last_bid,
                    'comment_form': comment_form,
                    'auction_is_closed': auction_is_closed
                })
            else:
                if new_bid.price <= last_bid.price:
                    return HttpResponse('<h2>The bid should be at least as the last bid, please put another bid</h2>')
                else:
                    new_bid.save()
                    return render(request, self.template_name,{
                    'listing': listing,
                    'comments': comments,
                    'bid_form': bid_form,
                    'bids': bids,
                    'new_bid': new_bid,
                    'last_bid': last_bid,
                    'comment_form': comment_form,
                    'auction_is_closed': auction_is_closed,
                    'new_comment': new_comment
                })

        
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
                'new_comment': new_comment,
                'comment_form': comment_form,
                'bid_form': bid_form,
                'auction_is_closed': auction_is_closed

            })
        return render(request, self.template_name,{
            'listing': listing,
            'comments': comments,
            'bids': bids,
            'last_bid': last_bid, 
            'bid_form': BidForm(),
            'comment_form': CommentForm(),
            'bid_form': bid_form,
            'auction_is_closed': auction_is_closed

        })
