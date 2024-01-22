from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isSeller = models.BooleanField()

    def __str__(self):
        return f"{self.user}"

class Ad(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=512)
    price = models.PositiveIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    isActive = models.BooleanField()
    image = models.CharField(max_length=128)
    type = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.title}"

class Review(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.poster} -> {self.seller}"

class Dispute(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    isSolved = models.BooleanField()

    def __str__(self):
        return f"{self.ad}: {self.user} disputing {self.ad.seller}"