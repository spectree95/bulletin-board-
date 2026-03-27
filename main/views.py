from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product,Liked,SubCategory
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

class Home(ListView):
    model = Product 
    context_object_name = 'products'
    template_name = 'main/base.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(category__title__icontains=q) |
                Q(phone__brand__icontains=q) |
                Q(phone__model__icontains=q)).distinct()
        
        return queryset

class ProductCreate(LoginRequiredMixin,CreateView):
    login_url = 'users/login'
    redirect_field_name = 'main/ProductCreate.html'
    success_url = reverse_lazy('main:Home')
    model = Product
    context_object_name = 'form'
    template_name = 'main/ProductCreate.html'
    fields = ['category','name','price','subcategory']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

def load_subcategories(request):

    category_id = request.GET.get("category")

    subcategories = SubCategory.objects.filter(category_id=category_id)

    data = list(subcategories.values("id", "name"))

    return JsonResponse(data, safe=False)


class MyProducts(LoginRequiredMixin,ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'main/MyProducts.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.request.user)
        return qs
            
class ProductDetail(DetailView):
    model = Product
    template_name = 'main/Product.html'
    context_object_name = 'product'

     
class ProductUpdate(LoginRequiredMixin,UpdateView):
    model = Product
    fields = ['category', 'title', 'price']
    template_name = 'main/ProductUpdate.html'
    success_url = reverse_lazy('main:home')
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)
     

class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'main/Product.html'
    success_url = reverse_lazy('main:home')
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)
    
@login_required
def ProductLike(request):
    if request.method == "POST":
        product_pk = request.POST.get('pk')
        product = Product.objects.get(id=product_pk)
        like, created = Liked.objects.get_or_create(
            user = request.user,
            product = product
        )
        if not created:
            like.delete()
            return JsonResponse({"favorited": False})
        return JsonResponse({"favorited": True})
    
class ProductLiked(LoginRequiredMixin, ListView):
    login_url = "users/login"
    redirect_field_name = "main/ProductLiked.html"
    
    model = Liked
    template_name = "main/ProductLiked.html"
    context_object_name = "likes"
    
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user = self.request.user)
        qs = qs.select_related("product")
        return qs