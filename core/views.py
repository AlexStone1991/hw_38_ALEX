# from .data import orders, services, masters
from .models import Order, Master, Service
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.context_processors import menu_items
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db.models import Q, Count, Sum

def about(request):
    # Здесь можно добавить логику для страницы "О нас"
    return render(request, 'about.html')

def landing(request):
# главная страница
    masters = Master.objects.filter(is_active=True).prefetch_related('services')[:6]
    reviews = Review.objects.filter(is_published=True).select_related('master')[:6]
    context = {
        'masters': masters,
        'reviews': reviews,
    }
    return render(request, 'landing.html', context)

def thanks(request):
    # Спасибо за заявку!
    return render(request, 'thanks.html')

@login_required # Декоратор проверяет, что пользователь авторизован
def orders_list(request):
    orders = Order.objects.prefetch_related("services").all()
    context = {
        "orders": orders
    }
    return render(request, 'orders_list.html', context=context)

@login_required
def order_detail(request, order_id):
    """
    Отвечает за маршрут 'orders/<int:order_id>/'
    :param request: HttpRequest
    :param order_id: int (номер заказа)
    """
    order = Order.objects.prefetch_related("services").select_related("master").annotate(total_price=Sum('services__price')).get(id=order_id)

    context = {"order": order}

    return render(request, "order_detail.html", context=context)
