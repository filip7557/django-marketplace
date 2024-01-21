from django.shortcuts import render
from django.urls import reverse
from .models import Ad

# Create your views here.
def home(request):
    sort = request.GET.get('filter', 'all')
    if(sort=='all'):
        ads = Ad.objects.order_by("-pub_date")
    else:
        ads = filter(lambda ad: ad.type == sort, Ad.objects.order_by("-pub_date"))
    context = {
        'ads': ads,
    }
    return render(request, 'marketplace/home.html', context)

def new(request): #treba ga napraviti
    return reverse('home')