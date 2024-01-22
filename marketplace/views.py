from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Ad, MarketplaceUser

# Create your views here.
def home(request):
    sort = request.GET.get('filter', 'all')
    if(sort=='all'):
        ads = filter(lambda ad: ad.isActive, Ad.objects.order_by("-pub_date"))
    else:
        ads = filter(lambda ad: ad.type == sort and ad.isActive, Ad.objects.order_by("-pub_date"))
    if request.user.is_authenticated:
        user = get_object_or_404(MarketplaceUser, pk=request.user.id)
    else:
        user = request.user
    context = {
        'ads': ads,
        'user': user,
    }
    return render(request, 'marketplace/home.html', context)

def buy(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method=="POST":
        id=request.POST['id']
        ad = get_object_or_404(Ad, pk=id)
        user = get_object_or_404(MarketplaceUser, pk=request.user.id)
        if user.credits >= ad.price:
            ad.isActive = False
            ad.save()
            user.credits -= ad.price
            user.save()
            #maybe add purchase model so we can save purchases
    return HttpResponseRedirect(reverse('home'))

def new(request): #treba ga napraviti
    return reverse('home')