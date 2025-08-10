from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomRegisterView,
    # CustomPasswordResetView,
    )
urlpatterns = [
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    # path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    ]