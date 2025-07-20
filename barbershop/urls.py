# barbershop\urls.py
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import landing, thanks, orders_list, order_detail, about, services_list, create_order, create_review, master_services_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('thanks/', thanks, name='thanks'),
    path('orders/', login_required(orders_list), name='orders'),
    path('orders/<int:order_id>/', login_required(order_detail), name='order_detail'),
    path('about/', about, name='about'),
    path("services/", services_list, name="services"),
    path('order/create/', create_order, name='create_order'),
    path("review/create/", create_review, name="create_review"),
    path('api/master/<int:master_id>/services/', master_services_api),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()