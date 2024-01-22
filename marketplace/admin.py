from django.contrib import admin
from .models import Ad, MarketplaceUser, Dispute, Review

# Register your models here.
admin.site.register(MarketplaceUser)
admin.site.register(Ad)
admin.site.register(Review)
admin.site.register(Dispute)