from django.forms import ModelForm
from django import forms


from .models import *

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['item_name', 'description', 'close_date', 'base_price', 'category', 'status', 'image']


class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['content']