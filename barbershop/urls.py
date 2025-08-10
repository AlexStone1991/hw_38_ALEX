# barbershop\urls.py
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import (
    LandingView,
    ThanksView,
    OrdersListView,
    OrderDetailView,
    OrderCreateView,
    ReviewCreateView,
    AboutView,
    ServicesListView,
    MasterServicesAPIView,
    ServiceMastersAPIView,
    MasterDetailView,
    
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingView.as_view(), name='landing'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('orders/', OrdersListView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('about/', AboutView.as_view(), name='about'),
    path("services/", ServicesListView.as_view(), name="services"),
    path('order/create/', OrderCreateView.as_view(), name='create_order'),
    path('review/create/', ReviewCreateView.as_view(), name='create_review'),
    path('api/master/<int:master_id>/services/', MasterServicesAPIView.as_view(), name='master_services_api'),
    path('api/service/<int:service_id>/masters/', ServiceMastersAPIView.as_view(), name='service_masters_api'),
    path('masters/<int:master_id>/', MasterDetailView.as_view(), name='master_detail'),
    path("users/", include("users.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()