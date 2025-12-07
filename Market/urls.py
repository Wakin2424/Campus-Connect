from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='market'),
    path('<str:category>', views.productLibrary, name='product_library'),
    path('sell-product/', views.uploadProduct, name='upload_product'),
    path('product/<str:id>/', views.productDetail, name='product_detail'),
]

