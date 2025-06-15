# core/views.py
from django.shortcuts import render, HttpResponse
from .data import orders, services, masters

def landing(request):
    """
    Отвечает за маршрут '/'
    """
    # Создаем структуру данных для услуг и мастеров
    services_with_masters = [
        {"name": "Стрижка под 'Горшок'", "masters": [masters[0]]},
        {"name": "Укладка 'Взрыв на макаронной фабрике'", "masters": [masters[1]]},
        {"name": "Королевское бритье опасной бритвой", "masters": [masters[2]]},
        {"name": "Окрашивание 'Жизнь в розовом цвете'", "masters": [masters[3]]},
        {"name": "Мытье головы 'Душ впечатлений'", "masters": [masters[4]]},
        {"name": "Стрижка бороды 'Боярин'", "masters": [masters[0], masters[2]]},
        {"name": "Массаж головы 'Озарение'", "masters": [masters[1], masters[3]]},
        {"name": "Укладка 'Ветер в голове'", "masters": [masters[4]]},
        {"name": "Плетение косичек 'Викинг'", "masters": [masters[0], masters[3]]},
        {"name": "Полировка лысины до блеска", "masters": [masters[2]]},
    ]

    context = {
        'masters': masters,
        'services_with_masters': services_with_masters,
    }
    return render(request, 'landing.html', context)

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
