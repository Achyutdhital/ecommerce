from django.contrib import admin
from .models import Address, Category, Product, Cart, Order ,WishlistItem,BlogPost ,Contacts,SocialMediaLink,HeroSection,ContactInfo


# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'locality', 'city', 'state')
    list_filter = ('city', 'state')
    list_per_page = 10
    search_fields = ('locality', 'city', 'state')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category_image', 'updated_at')
    list_per_page = 10
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title", )}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'product_image', 'updated_at')
    list_editable = ('slug', 'category' )
    list_per_page = 10
    search_fields = ('title', 'category', 'short_description')
    prepopulated_fields = {"slug": ("title", )}

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user', 'product')

class wishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product',  'created_at')
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user', 'product')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'status', 'ordered_date')
    list_editable = ('quantity', 'status')
    list_filter = ('status', 'ordered_date')
    list_per_page = 20
    search_fields = ('user', 'product')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title' , 'publish_date', 'image','uploader')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('firstname' , 'lastname', 'email','subject')

admin.site.register(Address, AddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(WishlistItem, wishlistAdmin)
admin.site.register(BlogPost, BlogAdmin)
admin.site.register(Contacts, ContactAdmin)
admin.site.register(SocialMediaLink)
admin.site.register(HeroSection)
admin.site.register(ContactInfo)





