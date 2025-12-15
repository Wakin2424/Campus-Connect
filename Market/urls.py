from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='market'),
    path('<str:category>', views.productLibrary, name='product_library'),
    path('sell-product/', views.uploadProduct, name='upload_product'),
    path('product/<str:id>/', views.productDetail, name='product_detail'),
    path('product/edit-product/<str:id>/', views.updateProductDetail, name='edit_product'),
    path('api/product/update-product/', views.saveProductChanges, name='update_product'),
]

