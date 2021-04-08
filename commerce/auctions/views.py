from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from .models import User, Auction
from .forms import AuctionForm, CommentForm




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
    if request.method == "POST":
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            item_name = form.cleaned_data["item_name"]
            description = form.cleaned_data["description"]
            close_date = form.cleaned_data["close_date"]
            base_price = form.cleaned_data["base_price"]
            category = form.cleaned_data["category"]
            status = form.cleaned_data["status"]
            image = form.cleaned_data["image"]
            # to get the user instance from the User model, This gives the logged in user 
            form.instance.user = request.user
            form.save()
            img_obj = form.instance
            return render(request, "auctions/create_listing.html",{
                'form': form,
                'img_obj': img_obj
            })
        else:
            return render(request, "auctions/create_listing.html",{
                'form': form
            })
            
    return render(request, "auctions/create_listing.html",{
        'form': AuctionForm()
    })

def auction_listings(request):
    
    listings = Auction.objects.filter(status=0).order_by('-posting_date')
    return render(request, "auctions/auction_listings.html",{
        'listings': listings  
    })

def listing_details(request, item_name):
    """
    Go to specific listing details
    """
    listing = get_object_or_404(Auction, item_name= item_name)
    comments = listing.comments.filter(active=True)
    new_comment = None
    # if the user post a comment
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # Assign the user who put the comment
            comment_form.instance.user_name = request.user

            # assign the current listing to the comment
            new_comment.listing = listing
            new_comment.save()

    else:
        comment_form = CommentForm()

    return render(request, "auctions/listing_details.html",{
        'listing': listing,
        'item_name': item_name,
        'comments' : comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })

    
