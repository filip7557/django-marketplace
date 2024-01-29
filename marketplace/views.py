from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Ad, Dispute, MarketplaceUser, Purchase

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
            ad.seller.credits += ad.price
            ad.seller.save()
            purchase = Purchase(buyer=request.user,seller=ad.seller, ad=ad,)
            purchase.save()
    return HttpResponseRedirect(reverse('home'))

def disputes(request):
    if request.user.is_superuser:
        sort = request.GET.get('filter', 'active') #we want to show active for default
        if(sort=='all'):
            disputes = Dispute.objects.order_by()
        elif(sort=='solved'):
            disputes = filter(lambda dispute: dispute.isSolved, Dispute.objects.order_by())
        elif(sort=='active'):
            disputes = filter(lambda dispute: not dispute.isSolved, Dispute.objects.order_by())
        context = {
            'disputes': disputes,
        }
        return render(request, 'marketplace/disputes.html', context)
    return HttpResponseRedirect(reverse('home'))

def solve_dispute(request):
    if request.user.is_superuser:
        if request.method=="POST":
            id=request.POST['id']
            dispute = get_object_or_404(Dispute, pk=id)
            dispute.isSolved = True
            dispute.save()
            return HttpResponseRedirect(reverse('marketplace:disputes'))
    return HttpResponseRedirect(reverse('home'))

def profile(request, user_id):
    if request.user.is_authenticated:
        clicked_user = get_object_or_404(MarketplaceUser, pk=user_id)
        if clicked_user.isSeller:
            reviews = clicked_user.review_set.all()
            if request.user.id == user_id: #seller checking out his own profile
                prev_sold_items = clicked_user.purchase_set.all()
                context = {
                    'seller': clicked_user,
                    'reviews': reviews,
                    'prev_sold_items': prev_sold_items,
                }
                return render(request, 'marketplace/seller_profile.html', context)
            #sellers public profile
            context = {
                'seller': clicked_user,
                'reviews': reviews,
            }
            return render(request, 'marketplace/seller_public_profile.html', context)
        elif request.user.id == user_id: #users own profile with prev purchases
            purchases = request.user.purchase_set.all()
            context = {
                'user': clicked_user,
                'purchases': purchases,
            }
            return render(request, 'marketplace/user_profile.html', context)
        return HttpResponseRedirect(reverse('home'))

def new(request): #treba ga napraviti
    return HttpResponseRedirect(reverse('home'))