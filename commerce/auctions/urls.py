from django.urls import path


from . import views

app_name = 'auctions'

urlpatterns = [
    # path("", views.index, name="index"),
    # path("", views.AuctionListView.as_view(), name="index"),
    path("", views.index, name="index"),
    path("<slug:category_slug>/", views.index, name="auctions_by_category"),
    path('<int:listing_id>/share_listing/', views.share_listing, name='share_listing'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction_listings", views.auction_listings, name= "auction_listings"),
    path("listing_details/<str:item_name>", views.listing_details.as_view(), name= "listing_details"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("add_to_watchlist/<int:listing_id>/", views.add_to_watchlist, name= "add_to_watchlist"),
    path("delete_listing/<int:listing_id>", views.delete_listing, name="delete_listing"),
    path("edit_listing/<int:listing_id>", views.edit_listing, name="edit_listing"),
    path("watchlist_items", views.watchlist_items, name= "watchlist_items")
]
