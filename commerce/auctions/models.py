from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from sorl.thumbnail import ImageField




STATUS = (
    (0,"Active"),
    (1,"Closed")
)

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)


    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    posting_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField()
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    status = models.IntegerField(choices=STATUS, default=0, blank=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return f"{self.user}, {self.item_name}, {self.status}"

    # To order the items based on the date they are posted. From the latest to oldest
    class Meta:
        ordering = ["-posting_date"]



class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Auction)

    def __str__(self):
        return f"{self.listing}, {self.user}"



class Bid(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userBids" , default=None)
    created_on = models.DateField(auto_now_add=True, blank=True, null=True)
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE,related_name='bids')
   # number_of_bids = models.IntegerField(blank=True, null=True)
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'{self.price}$, placed by {self.user_name}'


class Comments(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"comment by: {self.user_name} on {self.listing}"


