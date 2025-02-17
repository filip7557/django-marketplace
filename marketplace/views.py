from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import UserForm
from .models import Ad, Dispute, MarketplaceUser, Purchase, Review

# Create your views here.
def home(request):
    sort = request.GET.get('filter', 'all')
    if(sort=='all'):
        ads = filter(lambda ad: ad.isActive, Ad.objects.order_by("-pub_date"))
    else:
        ads = filter(lambda ad: ad.type == sort and ad.isActive, Ad.objects.order_by("-pub_date"))
    if request.user.is_authenticated:
        user = get_object_or_404(MarketplaceUser, user=request.user)
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

def dispute(request, ad_id):
    if request.user.is_authenticated:
        ad=get_object_or_404(Ad, pk = ad_id)
        if request.method=="POST":
            user = request.user
            text = request.POST['text']
            
            Dispute.objects.create(ad = ad, user = user, text = text, isSolved = False)

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
                purchases = request.user.purchase_set.all()
                context = {
                    'seller': clicked_user,
                    'reviews': reviews,
                    'prev_sold_items': prev_sold_items,
                    'purchases': purchases,
                }
                return render(request, 'marketplace/seller_profile.html', context)
            #sellers public profile
            context = {
                'seller': clicked_user,
                'seller_id': user_id, 
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
    
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            # We need to set the password separately, because the UserForm
            # doesn't have a password field, it uses two fields for the password
            # and password confirmation.
            user = User.objects.create_user(user_form.cleaned_data['username'], None, user_form.cleaned_data['password1'])

            select = request.POST['isSeller']
            if(select=="yes"):
                isSeller = True
            else:
                isSeller = False

            # We need to set the user field on marketplaceUser before we can save it
            MarketplaceUser.objects.create(user=user, isSeller=isSeller, credits=0)
            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, 'registration/register.html', {'user_form': user_form,})
    else:
        user_form = UserForm()
        return render(request, 'registration/register.html', {'user_form': user_form})

def new(request): 
    if request.user.is_authenticated:
        user = get_object_or_404(MarketplaceUser, pk=request.user.id)
        if request.method=="POST":
            if(user.isSeller):
                title=request.POST['title'] 
                desc=request.POST['desc'] 
                price=request.POST['price']
                image=request.POST['image']
                type=request.POST['type']

                ad=Ad(title = title,desc = desc,price = price, seller = user,isActive=True,image = image, type = type)
                ad.save()   
            return HttpResponseRedirect(reverse('home'))
        else:
            if(not user.isSeller):
                context = {}
                return render(request, 'marketplace/user_not_seller.html', context)
            context={}
            return render(request, 'marketplace/new.html', context)
    else:
            return HttpResponseRedirect(reverse('home'))

def review(request, seller_id): 
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.id)
        if request.method=="POST":
                seller = get_object_or_404(MarketplaceUser, pk=seller_id)
                rating = request.POST['rating']
                text = request.POST['text']

                review = Review(poster = user, seller = seller, rating = rating, text = text)
                review.save()   
                
        
    return HttpResponseRedirect(reverse('marketplace:profile', args=(seller_id,)))
            