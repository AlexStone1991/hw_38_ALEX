# barbershop/urls.py
from django.contrib import admin
from django.urls import path
from core.views import landing, thanks, orders_list, order_details

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('thanks/', thanks, name='thanks'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/<int:order_id>/', order_details, name='order_details'),
]
