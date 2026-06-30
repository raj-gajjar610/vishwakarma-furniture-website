"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from .views import category

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.index),
                  path('about', views.about),
                  path('project', views.project),
                  path('services', views.services),
                  path('login', views.login),
                  path('contact', views.contact),
                  path('blogsingle', views.blogsingle),
                  path('blog', views.blog),
                  path('product', views.product),
                  path('signup', views.signup),
                  path('category', views.category, ),
                  path('subcategory/<int:c_id>/', views.subcategory),
                  path('product_detail/<int:id>/', views.product_detail),
                  # all cart urls
                  path('add_to_cart/<int:id>/', views.add_to_cart),
                  path('view_cart',views.view_cart),
                  path('remove_cart/<int:id>/', views.remove_cart),
                  path('increase_qty/<int:id>/', views.increase_qty, name='increase_qty'),
                  path('decrease_qty/<int:id>/', views.decrease_qty, name='decrease_qty'),
                  #all wishlist urls
                  path('add_to_wishlist/<int:id>/', views.add_to_wishlist),
                  path('wishlist', views.wishlist),
                  path('remove_wishlist/<int:id>/', views.remove_wishlist),
                  #payment method
                  path('checkout/', views.checkout, name='checkout'),
                  path('razorpay-order/', views.create_razorpay_order),
                  #search bar
                  path('search/', views.search_products),
                  #your order
                  path('your-order/', views.your_order, name='your_order'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

