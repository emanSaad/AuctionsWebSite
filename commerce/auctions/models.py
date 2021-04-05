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
    

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    posting_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField()
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=100, default="no category", blank=True)
    status = models.IntegerField(choices=STATUS, default=0, blank=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return f"{self.user}, {self.item_name}, {self.status}"

    # To order the items based on the date they are posted. From the latest to oldest
    class Meta:
        ordering = ["-posting_date"]


class Bids(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    name = models.ManyToManyField(User)
    time = models.DateField()
    item = models.ForeignKey(Auction, on_delete=models.CASCADE)
    number_of_bids = models.IntegerField()

    def __str__(self):
        return f"{self.bid_item}, {self.bid_price}, {self.bidder_name}, {self.number_of_bids}"


class Comments(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateField(default=timezone.now)
    content = models.CharField(max_length=100)
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.name}, {self.created_on}, {self.listing}"


