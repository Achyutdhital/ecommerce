from django.urls import path
from . import views
from django.urls import re_path
from django.contrib.auth import views as auth_views
from .views import error_400_view


app_name = 'app2'

urlpatterns = [
    path('home', views.DashboardView.as_view(), name='home'),
    path('login/', views.App2LoginView.as_view(), name='app2login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='app2:app2login'), name="app2logout"),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add_edit/', views.ProductAddEditView.as_view(), name='add_edit_product'),
    path('products/add_edit/<slug:product_slug>/', views.ProductAddEditView.as_view(), name='add_edit_product'),
    path('products/delete/<slug:product_slug>/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('blog_post/', views.BlogPostListView.as_view(), name='blog_post_list'),
    path('blog_post/add_edit/', views.BlogPostAddEditView.as_view(), name='add_edit_blog_post'),
    path('blog_post/add_edit/<slug:blog_post_slug>/', views.BlogPostAddEditView.as_view(), name='add_edit_blog_post'),
    path('blog_post/delete/<slug:blog_post_slug>/', views.BlogPostDeleteView.as_view(), name='delete_blog_post'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add_edit/', views.CategoryAddEditView.as_view(), name='add_edit_category'),
    path('categories/add_edit/<slug:category_slug>/', views.CategoryAddEditView.as_view(), name='add_edit_category'),
    path('categories/delete/<slug:category_slug>/', views.CategoryDeleteView.as_view(), name='delete_category'),
    path('order/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('cart/list/', views.CartListView.as_view(), name='cart_list'),
    path('wishlist/list/', views.WishlistItemListView.as_view(), name='wishlist_item_list'),
    path('contacts/list/', views.ContactListView.as_view(), name='contact_list'),
    path('<path:not_found>', error_400_view, name='catch_all_404'),


]

handler400 = error_400_view
