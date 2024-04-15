import django
from django.contrib.auth.models import User  
from .models import*
from django.shortcuts import redirect, render, get_object_or_404 ,HttpResponseRedirect
from .forms import RegistrationForm, AddressForm
from django.contrib import messages
from django.views import View
import decimal
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator # for Class Based Views
from .forms import ContactForm 
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.messages import get_messages
from rest_framework import viewsets
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Create your views here.

def home(request):
    categories = Category.objects.all()[:3]
    products = Product.objects.all()[:8]
    hero_section = HeroSection.objects.first()
    if request.user.is_authenticated:
        user_wishlist = WishlistItem.objects.filter(user=request.user, product__in=products).values_list('product__id', flat=True)
    else:
        user_wishlist = []
    if request.user.is_authenticated:
        cart_product_ids = Cart.objects.filter(user=request.user).values_list('product__id', flat=True)
    else:
        cart_product_ids = []
    context = {
        'categories': categories,
        'products': products,
        'is_in_wishlist': user_wishlist,
        'cart_product_ids':cart_product_ids,
        'user': request.user,
        'hero_section':hero_section,
    }
    return render(request, 'app/index.html', context)


def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.exclude(id=product.id).filter(category=product.category)
    user_wishlist = False  # Initialize with False
    if request.user.is_authenticated:
        user_wishlist = WishlistItem.objects.filter(user=request.user, product=product).exists()

    if request.user.is_authenticated:
        cart_product_ids = Cart.objects.filter(user=request.user).values_list('product__id', flat=True)
    else:
        cart_product_ids = []
    context = {
        'product': product,
        'related_products': related_products,
        'is_in_wishlist': user_wishlist,
        'cart_product_ids':cart_product_ids,
        'user': request.user,

    }
    return render(request, 'app/detail.html', context)


def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'app/categories.html', {'categories':categories})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category_slug = request.GET.get('category')
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'latest') 
    sort_order = request.GET.get('sort_order', 'desc') 
    if request.user.is_authenticated:
        user_wishlist = WishlistItem.objects.filter(user=request.user, product__in=products).values_list('product__id', flat=True)
    else:
        user_wishlist = []
    
    if request.user.is_authenticated:
        cart_product_ids = Cart.objects.filter(user=request.user).values_list('product__id', flat=True)
    else:
        cart_product_ids = []

    if query:
        products = products.filter(Q(title__icontains=query))

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if sort_by == 'name':
        if sort_order == 'asc':
            products = products.order_by('title')
        elif sort_order == 'desc':
            products = products.order_by('-title')
    elif sort_by == 'latest':
        if sort_order == 'asc':
            products = products.order_by('created_at')
        elif sort_order == 'desc':
            products = products.order_by('-created_at')  
    elif sort_by == 'price':
        if sort_order == 'asc':
            products = products.order_by('price')
        elif sort_order == 'desc':
            products = products.order_by('-price')
    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'is_in_wishlist': user_wishlist,
        'cart_product_ids':cart_product_ids,
        'user': request.user,
    }
    return render(request, 'app/category_products.html', context)


# Authentication Starts Here

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'app/register.html', {'form': form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations! Registration Successful!")
            form.save()
        return render(request, 'app/register.html', {'form': form})
        

@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'app/profile.html', {'addresses':addresses, 'orders':orders})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        
        return render(request, 'app/add_address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user=request.user
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            reg = Address(user=user, locality=locality, city=city, state=state)
            reg.save()
            messages.success(request, "New Address Added Successfully.")
            next_url = request.POST.get('next')
            next_param = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            return redirect('app:profile')
        return render(request, 'app/add_address.html', {'form': form,
                                                        'next': next_param})


@login_required
def remove_address(request, id):
    a = get_object_or_404(Address, user=request.user, id=id)
    a.delete()
    messages.success(request, "Address removed.")
    return redirect('app:profile')

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    # Check whether the Product is alread in Cart or Not
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        # cp.quantity += 1
        # cp.save()
        cp.delete()

    else:
        Cart(user=user, product=product).save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(10)
    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    addresses = Address.objects.filter(user=user)

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
    }
    return render(request, 'app/cart.html', context)


@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
    return redirect('app:cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('app:cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('app:cart')


@login_required
def checkout(request):
    user = request.user
    address_id = request.GET.get('address')
    
    print("Address ID:", address_id)
    print("Request GET:", request.GET)

    if address_id:
        address = get_object_or_404(Address, id=address_id)
        cart = Cart.objects.filter(user=user)
        
        for c in cart:
            Order.objects.create(user=user, address=address, product=c.product, quantity=c.quantity )
            c.delete()

        return redirect('app:orders')
    else:
        messages.warning(request, "Please select a shipping address.")
        return redirect('app:cart')


@login_required
def orders(request):
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'app/orders.html', {'orders': all_orders})





def shop(request ):
    gender = request.GET.get('gender')
    category_slug = request.GET.get('category')
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'latest') 
    sort_order = request.GET.get('sort_order', 'desc') 
    products = Product.objects.all()

    
    if query:
        products = products.filter(Q(title__icontains=query))

    if gender:
        products = products.filter(gender=gender)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if sort_by == 'name':
        if sort_order == 'asc':
            products = products.order_by('title')
        elif sort_order == 'desc':
            products = products.order_by('-title')
    elif sort_by == 'latest':
        if sort_order == 'asc':
            products = products.order_by('created_at')
        elif sort_order == 'desc':
            products = products.order_by('-created_at')  
    elif sort_by == 'price':
        if sort_order == 'asc':
            products = products.order_by('price')
        elif sort_order == 'desc':
            products = products.order_by('-price')

    if request.user.is_authenticated:
        user_wishlist = WishlistItem.objects.filter(user=request.user, product__in=products).values_list('product__id', flat=True)
    else:
        user_wishlist = []
    
    if request.user.is_authenticated:
        cart_product_ids = Cart.objects.filter(user=request.user).values_list('product__id', flat=True)
    else:
        cart_product_ids = []

    categories = Category.objects.all()
    page = request.GET.get('page', 1)
    items_per_page = 9  # Number of items to display per page

    paginator = Paginator(products, items_per_page )
    products = paginator.get_page(page)

    context = {
        'products': products,
        'categories': categories,
        'is_in_wishlist': user_wishlist,
        'cart_product_ids':cart_product_ids,
        'user': request.user,
        'paginator':paginator,
    }
    return render(request, 'app/shop.html' ,context)

def filter_by_gender_category(request, gender_slug, category_slug):
    gender = dict(Product.GENDER_CHOICES).get(gender_slug)
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(gender=gender, category=category)
    categories = Category.objects.all()
    
    return render(request, 'shop.html', {'products': products, 'categories': categories})


@login_required
def add_to_wishlist(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        wishlist_item.delete()

    # Redirect back to the referring page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def wishlist(request):
    products = Product.objects.all()

    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user)
        wishlist_count = wishlist_items.count()
    else:
        wishlist_items = []
        wishlist_count = 0

    if request.user.is_authenticated:
        user_wishlist = WishlistItem.objects.filter(user=request.user, product__in=products).values_list('product__id', flat=True)
    else:
        user_wishlist = []
    
    if request.user.is_authenticated:
        cart_product_ids = Cart.objects.filter(user=request.user).values_list('product__id', flat=True)
    else:
        cart_product_ids = []

    context = {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_count,
        'is_in_wishlist': user_wishlist,
        'cart_product_ids':cart_product_ids,
    }
    return render(request, 'app/wishlist.html', context)


def blog(request):
    sort_by = request.GET.get('sort_by', 'latest') 
    blog_posts = BlogPost.objects.all()

    if sort_by == 'oldest':
        blog_posts = blog_posts.order_by('publish_date')
    elif sort_by == 'latest':
        blog_posts = blog_posts.order_by('-publish_date')  

    paginator = Paginator(blog_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sort_by': sort_by,
    }
    return render(request, 'app/blog.html', context)

def blog_detail(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug)
    context = {
        'blog_post': blog_post
    }
    return render(request, 'app/blog_detail.html', context)

def contact(request):
    if request.method =="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            subject = request.POST['subject']
            message1 = request.POST['message']
            emaild = request.POST['email']

            subject1 = "New response in contact"
            message2 = f"customer details:"+"Name:"+firstname+" "+lastname+" " +"email:"+emaild +"  "+ "subject:"+subject +"  "+ "message:"+message1
            email_from1= settings.EMAIL_HOST_USER
            emailto = ["hermansepherd@gmail.com"]
            send_mail(subject1,message2,email_from1, emailto)


            email = request.POST['email']
            subject = "Message submitted sucessfully"
            message = "Thank you for reaching to us. We will contact you shortly"
            email_from = settings.EMAIL_HOST_USER
            to = [email]
            send_mail(subject,message,email_from,to)
            
            messages.success(request , "sucess!!")
            return redirect("app:contact")
    # else:
    #     messages.error(request, "response not submitted!!")
    #     contact = ContactForm()
    #     return render (request ,'app/contact.html', {'form': contact,
    #                                                })
        else:
            messages.error(request, "response not submitted!!")
    else:
        form = ContactForm()
    
    storage = get_messages(request)
    for message in storage:
        pass
    
    return render(request, 'app/contact.html', {'form': form})


def test(request):
    return render(request, 'app/test.html')

def error_400_view(request, not_found):
    return render(request, 'app/404.html', status=404)



from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
