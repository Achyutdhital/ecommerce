from .forms import LoginForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from .views import error_400_view
from rest_framework import routers
from .views import ProductViewSet

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)


app_name = 'app'


urlpatterns = [
    path('', views.home, name="home"),
    #api practice
    path('api/', include(router.urls)),

    path('api/product/', views.product_list),
    path('api/product/<int:pk>/', views.product_detail),
    #end api practice lines
    
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('remove-cart/<int:cart_id>/', views.remove_cart, name="remove-cart"),
    path('plus-cart/<int:cart_id>/', views.plus_cart, name="plus-cart"),
    path('minus-cart/<int:cart_id>/', views.minus_cart, name="minus-cart"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('orders/', views.orders, name="orders"),
    #URL for Products
    path('product/<slug:slug>/', views.detail, name="product-detail"),
    path('categories/', views.all_categories, name="all-categories"),
    path('shop/', views.shop, name="shop"),
    # URL for Authentication
    path('app/register/', views.RegistrationView.as_view(), name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name="login"),
    path('app/profile/', views.profile, name="profile"),
    path('app/add-address/', views.AddressView.as_view(), name="add-address"),
    path('app/remove-address/<int:id>/', views.remove_address, name="remove-address"),
    path('app/logout/', auth_views.LogoutView.as_view(next_page='app:login'), name="logout"),

    path('app/password-change/', auth_views.PasswordChangeView.as_view(template_name='app/password_change.html', form_class=PasswordChangeForm, success_url='/app/password-change-done/'), name="password-change"),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='app/password_change_done.html'), name="password-change-done"),

    path('app/password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=PasswordResetForm, success_url='/app/password-reset/done/'), name="password-reset"), # Passing Success URL to Override default URL, also created password_reset_email.html due to error from our app_name in URL
    path('app/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name="password_reset_done"),
    path('app/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=SetPasswordForm, success_url='/app/password-reset-complete/'), name="password_reset_confirm"), # Passing Success URL to Override default URL
    path('app/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name="password_reset_complete"),

    path('product/test/', views.test, name="test"),
    path('add-to-wishlist/<int:prod_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('shop/<slug:gender_slug>/category/<slug:category_slug>/', views.filter_by_gender_category, name='filter-by-gender-category'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog-detail'),
    path('contact', views.contact, name='contact'),
    path('wishlist/', views.wishlist, name='wishlist'),


    path('<slug:slug>/', views.category_products, name="category-products"),
    
    # path('<path:not_found>', error_400_view, name='catch_all_404'),

    
] 
# handler401 = error_400_view
