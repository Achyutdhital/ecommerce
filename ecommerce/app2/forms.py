from django import forms
from app.models import*
from django.contrib.auth.forms import  AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class App2LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

