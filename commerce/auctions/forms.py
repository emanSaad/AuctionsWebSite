from django.forms import ModelForm
from django import forms


from .models import *

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['item_name', 'description', 'close_date', 'base_price', 'status', 'image','category']
        # exclude = ('category', ) 

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['content']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']

# class CategoryForm(forms.ModelForm):
#     categories = forms.ModelMultipleChoiceField(
#         queryset=Category.objects.all().values('name'),
#         required=True,
#         )
#     class Meta:
#         model = Category
#         fields = ['name']



# form for sharing listing
class EmailLisingForm(forms.Form):
    name = forms.CharField(max_length=25)
    email= forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)