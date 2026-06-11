from django.urls import path
from . import views
from .views import Home,DetailCategory,Search_view, ProductCreate,SubCategoryProducts, MyProducts, ProductDetail,ProductLiked, ProductUpdate,ProductDelete
app_name = 'main'

urlpatterns = [
    path('',Home.as_view(), name='home'),
    path("Search", Search_view.as_view(),name="SearchView"),
    path("ProductCreate", ProductCreate.as_view(), name='ProductCreate'),
    path("MyProducts", MyProducts.as_view(), name='MyProducts'),
    path("Product/<int:pk>", ProductDetail.as_view(), name='Product'),
    path('ProductUpdate/<int:pk>/Update', ProductUpdate.as_view(), name='ProductUpdate'),
    path('ProductDelete/<int:pk>/Delete', ProductDelete.as_view(), name='ProductDelete'),
    path("Like/", views.ProductLike, name="ProductLike"),
    path("ProductLiked/", ProductLiked.as_view(), name="ProductLiked"),
    path("ajax/load-subcategories/", views.load_subcategories, name="ajax_load_subcategories"),
    path("ajax/load-attributes/", views.load_attributes, name="ajax_load-attributes/"),
    path("category/<int:pk>",DetailCategory.as_view(),name='category' ),
    path("products/<int:pk>", SubCategoryProducts.as_view(), name="SubCategoryProducts")
]
