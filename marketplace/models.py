from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isSeller = models.BooleanField

class Ad(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=512)
    pub_date = models.DateTimeField
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    isActive = models.BooleanField
    image = models.CharField(max_length=128)
    type = models.CharField(max_length=128)

class Review(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    rating = models.IntegerField
    text = models.CharField(max_length=512)

class Dispute(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    isSolved = models.BooleanField