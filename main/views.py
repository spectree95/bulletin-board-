from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category,Product,ProductImage, Liked,SubCategory,Attribute, AttributeValue
from django.db.models import Q, Exists,OuterRef
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import AttributeValueFormSet

class Home(ListView):
    model = Product 
    context_object_name = 'products'
    template_name = 'main/base.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(category__name__icontains=q) |
                Q(subcategory__name__icontains=q)).distinct()
        
       
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()
        return context

class ProductCreate(LoginRequiredMixin,CreateView):
    login_url = 'users/login'
    redirect_field_name = 'main/ProductCreate.html'
    success_url = reverse_lazy('main:home')
    model = Product
    context_object_name = 'form'
    template_name = 'main/ProductCreate.html'
    fields = ['category','name','price','subcategory','description']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        return context
    
    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        category = self.request.POST.get("category")
        if category:
            form.fields["subcategory"].queryset = SubCategory.objects.filter(category=category)
        else:    
            form.fields["subcategory"].queryset = SubCategory.objects.none()
        
        return form
    
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        for key, value in self.request.POST.items():
            if key.startswith("attribute_"):
                attribute_id = key.split("_")[1]

                AttributeValue.objects.create(
                    product=self.object,
                    attribute_id=attribute_id,
                    value=value
                )
        images = self.request.FILES.getlist('images')
        for img in images:
            ProductImage.objects.create(
                product = self.object,
                image = img
            )
        

        return response
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
    
        

def load_subcategories(request):

    category = request.GET.get("category")

    subcategories = SubCategory.objects.filter(category=category)

    data = list(subcategories.values("id", "name"))

    return JsonResponse(data, safe=False)


def load_attributes(request):
    subcategory = request.GET.get("subcategory")
    attributes = Attribute.objects.filter(subcategory = subcategory)
    data = list(attributes.values("id","name"))
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

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            likes = Liked.objects.filter(
                user = self.request.user,
                product = OuterRef("pk") 
            )
            queryset = queryset.annotate(is_liked=Exists(likes))
        
        return queryset

     
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
    
def ProductLike(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "auth"}, status=401)
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
    
    
class DetailCategory(DetailView):
    model = Category
    context_object_name = "category"
    template_name = "main/category.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subcategories"] = SubCategory.objects.filter(category=self.object)
        return context
    
class SubCategoryProducts(DetailView):
    model = SubCategory
    context_object_name = "subcategory"
    template_name = "main/SubCategory_products.html"
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(subcategory=self.object)
        if self.request.user.is_authenticated:
            likes = Liked.objects.filter(
                user = self.request.user,
                product = OuterRef("pk")
            )
            products = products.annotate(is_liked=Exists(likes))
        context["products"] = products
        return context 
        