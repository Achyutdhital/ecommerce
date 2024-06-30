from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from app.models import*
from django.shortcuts import redirect, render, get_object_or_404 ,HttpResponseRedirect
from django.views import View
from .forms import*
from django.core.files import File
from django.db.models import Subquery, OuterRef
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import superadmin_required
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse



def is_superuser(user):
    return user.is_authenticated and user.is_superuser


class App2LoginView(LoginView):
    template_name = 'app2/login.html'
    authentication_form = App2LoginForm 
    def form_invalid(self, form):
        if not self.request.user.is_superuser:
            url = reverse('app2:app2login')
            return HttpResponseRedirect(url + '?next=' + self.request.GET.get('next', '') + '&error=admin')
        
        return super().form_invalid(form)


@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class DashboardView(TemplateView):
    template_name = 'app2/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class ProductListView(View):
    def get(self, request):
        search_query = request.GET.get('q')
        sort_by = request.GET.get('sort_by', '-created_at')
        category_slug = request.GET.get('category')
        gender = request.GET.get('gender')
        page_number = request.GET.get('page', 1) 
       

        products = Product.objects.all()

        if search_query:
            products = products.filter(
                Q(title__icontains=search_query) |
                Q(category__title__icontains=search_query)
            )


        if gender:
            products = products.filter(gender=gender)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        products = products.order_by(sort_by)
        categories = Category.objects.all()
        paginator = Paginator(products, 10) 
        page = paginator.get_page(page_number)

        context = {'page':page,
                   'categories': categories,

                   }
        return render(request, 'app2/product_list.html', context)

@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class ProductAddEditView(View):
    def get(self, request,  product_slug=None):
        if product_slug:
            product = get_object_or_404(Product, slug=product_slug)
            form = ProductForm(instance=product)
        else:
            form = ProductForm()

        return render(request, 'app2/product_edit.html', {'form': form})

    def post(self, request, product_slug=None):
        if product_slug:
            product = get_object_or_404(Product, slug=product_slug)
            form = ProductForm(request.POST, request.FILES, instance=product)
        else:
            form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)

            new_image = form.cleaned_data.get('product_image')
            if new_image:
                instance.product_image.save(new_image.name, new_image, save=False)

            instance.save()

            return redirect('app2:product_list')

        return render(request, 'app2/product_edit.html', {'form': form})

@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class ProductDeleteView(View):
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        return render(request, 'app2/product_delete_confirm.html', {'product': product})

    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        product.delete()
        return redirect('app2:product_list')
    
@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class BlogPostListView(View):
    def get(self, request):
        search_query = request.GET.get('q')
        sort_by = request.GET.get('sort_by', '-publish_date')
        page_number = request.GET.get('page', 1) 

        blog_posts = BlogPost.objects.all()

        if search_query:
            blog_posts = blog_posts.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        blog_posts = blog_posts.order_by(sort_by)

        paginator = Paginator(blog_posts, 10) 
        page = paginator.get_page(page_number)

        return render(request, 'app2/blog_post_list.html', {'page': page})

@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class BlogPostAddEditView(View):
    def get(self, request, blog_post_slug=None):
        if blog_post_slug:
            blog_post = get_object_or_404(BlogPost, slug=blog_post_slug)
            form = BlogPostForm(instance=blog_post)
        else:
            form = BlogPostForm()

        return render(request, 'app2/blog_post_edit.html', {'form': form})

    def post(self, request, blog_post_slug=None):
        if blog_post_slug:
            blog_post = get_object_or_404(BlogPost, slug=blog_post_slug)
            form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        else:
            form = BlogPostForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save()
            return redirect('app2:blog_post_list')

        return render(request, 'app2/blog_post_edit.html', {'form': form})
    
    
@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class BlogPostDeleteView(View):
    def get(self, request, blog_post_slug):  
        post = get_object_or_404(BlogPost, slug=blog_post_slug)
        return render(request, 'app2/blog_delete_confirm.html', {'post': post})

    def post(self, request, blog_post_slug):
        post = get_object_or_404(BlogPost, slug=blog_post_slug)
        post.delete()
        return redirect('app2:blog_post_list')


@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class CategoryListView(View):
    def get(self, request):
        # Get query parameters for search and sorting
        search_query = request.GET.get('q')
        sort_by = request.GET.get('sort_by', '-created_at')
        page_number = request.GET.get('page', 1)  # Default to page 1

        categories = Category.objects.all()

        if search_query:
            categories = categories.filter(title__icontains=search_query)

        categories = categories.order_by(sort_by)

        paginator = Paginator(categories, 10)  # 10 items per page
        page = paginator.get_page(page_number)

        return render(request, 'app2/category_list.html', {'page': page})

@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class CategoryAddEditView(View):
    def get(self, request, category_slug=None):
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            form = CategoryForm(instance=category)
        else:
            form = CategoryForm()

        return render(request, 'app2/category_edit.html', {'form': form})

    def post(self, request, category_slug=None):
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            form = CategoryForm(request.POST, request.FILES, instance=category)
        else:
            form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('app2:category_list')

        return render(request, 'app2/category_edit.html', {'form': form})

@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class CategoryDeleteView(View):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        return render(request, 'app2/category_delete_confirm.html', {'category': category})

    def post(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        category.delete()
        return redirect('app2:category_list')

@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class OrderDetailView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        return render(request, 'app2/order_detail.html', {'order': order})
    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        return redirect('app2:order_list')

@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class OrderListView(View):
    def get(self, request):
        latest_orders = Order.objects.order_by('-ordered_date')
        
        paginator = Paginator(latest_orders, 10)  # 10 items per page
        page_number = request.GET.get('page', 1)  # Default to page 1
        page = paginator.get_page(page_number)

        return render(request, 'app2/order_list.html', {'page': page})

@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class CartListView(View):
    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        paginator = Paginator(cart_items, 10)  # 10 items per page
        page_number = request.GET.get('page', 1)  # Default to page 1
        page = paginator.get_page(page_number)

        return render(request, 'app2/cart_list.html', {'page': page})

@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class WishlistItemListView(View):
    def get(self, request):
        user = request.user
        wishlist_items = WishlistItem.objects.filter(user=user)

        paginator = Paginator(wishlist_items, 10)  # 10 items per page
        page_number = request.GET.get('page', 1)  # Default to page 1
        page = paginator.get_page(page_number)

        return render(request, 'app2/wishlist_item_list.html', {'page': page})

@method_decorator([login_required(login_url='app2:app2login'), superadmin_required], name='dispatch')
class ContactListView(View):
    def get(self, request):
        contacts = Contacts.objects.all()

        paginator = Paginator(contacts, 10)  # 10 items per page
        page_number = request.GET.get('page', 1)  # Default to page 1
        page = paginator.get_page(page_number)

        return render(request, 'app2/contact_list.html', {'page': page})
    
def error_400_view(request, not_found):
    return render(request, 'app2/error_400.html', status=404)