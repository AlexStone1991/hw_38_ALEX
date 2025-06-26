# barbershop\urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from core.views import landing, thanks, orders_list, order_detail, about, all_services, all_masters, appointment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('thanks/', thanks, name='thanks'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('about/', about, name='about'),
    path('services/', all_services, name='services'),
    path('masters/', all_masters, name='masters'),
    path('appointment/', appointment, name='appointment'),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])