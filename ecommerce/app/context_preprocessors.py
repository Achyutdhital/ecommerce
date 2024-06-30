from .models import Category, Cart ,WishlistItem,SocialMediaLink,ContactInfo


def store_menu(request):
    categories = Category.objects.filter(is_active=True)
    context = {
        'categories_menu': categories,
    }
    return context

def cart_menu(request):
    if request.user.is_authenticated:
        cart_items= Cart.objects.filter(user=request.user)
        context = {
            'cart_items': cart_items,
        }
    else:
        context = {}
    return context

def wishlist_count(request):
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user)
        wishlist_count = wishlist_items.count()
    else:
        wishlist_count = 0

    return {'wishlist_count': wishlist_count}

def social_links(request):
    links = SocialMediaLink.objects.all()
    return {'social_media_links': links}

def contact_info(request):
    contact_info = ContactInfo.objects.first()  
    return {'contact_info': contact_info}