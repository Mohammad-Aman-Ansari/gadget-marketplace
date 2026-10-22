from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sell/', views.sell_gadget, name='sell_gadget'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
]