from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction_listings", views.auction_listings, name= "auction_listings"),
    path("listing_details/<str:item_name>", views.listing_details.as_view(), name= "listing_details"),
    path("create_listing", views.create_listing, name="create_listing")
]
