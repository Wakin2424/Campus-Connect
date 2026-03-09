from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='market'),
    path('library/', views.productLibrary, name='product_library'),
    path('api/products/', views.loadProducts, name='product_library_content'),
    path('sell-product/', views.uploadProduct, name='upload_product'),
    path('product/', views.productDetail404, name='product_detail'),
    path('product/<str:id>/', views.productDetail, name='product_detail'),
    path('product/edit-product/<str:id>/', views.updateProductDetail, name='edit_product'),
    path('api/product/update-product/', views.saveProductChanges, name='update_product'),
]

