from django.urls import path
from . import views

urlpatterns = [
    path('payment_success/', views.payment_success, name='payment_success'),
    path('checkout/', views.checkout, name='checkout'),
    path('billing_info/', views.billing_info, name='billing_info'),
    path('process_order/', views.process_order, name='process_order'),
    path('item_list/', views.item_list, name='item_list'),
    path('orders/<int:pk>', views.orders, name='orders'),
    path('user_list/', views.user_list, name='user_list'),
    path('users_courses/<int:pk>', views.users_courses, name='users_courses'),
]