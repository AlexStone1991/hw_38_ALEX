# core/views.py
from django.shortcuts import render, HttpResponse
from .data import orders, services, masters

def landing(request):
    """
    Отвечает за маршрут '/'
    """
    сontext = {
        "masters": masters,
        "services": services,
    }
    return render(request, 'landing.html', сontext)

def thanks(request):
    """
    Отвечает за маршрут  '/thanks/'
    """
    return render(request, 'thanks.html')

def orders_list(request):
    """
    Отвечает за маршрут /orders/'
    """
    context = {
        "orders": orders,
    }
    return render(request, 'orders_list.html', context=context)

def order_details(request, order_id):
    """
    Отвечает за маршрут /orders/<int:order_id>/
    :param request: HttpRequest
    :param order_id: int (номер заказа)
    """
    order = next((order for order in orders if order['id'] == order_id), None) 
    # Использует next для поиска заказа по order_id, что делает код более читаемым.
    if order is None:
        return render (request, "order_not_found.html", {"order_id": order_id}, status=404)
    
    context = {
        "order": order,
    }

    return render(request, 'order_details.html', context=context)
