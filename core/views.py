from django.shortcuts import render
from .data import orders, services, masters

def about(request):
    return render(request, 'about.html')

def services(request):
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
        'services_with_masters': services_with_masters,
    }
    return render(request, 'services.html', context=context)

def all_masters(request):
    context = {
        'masters': masters,
    }
    return render(request, 'masters.html', context=context)

def appointment(request):
    return render(request, 'appointment.html')

def landing(request):
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
    return render(request, 'thanks.html')

def orders_list(request):
    context = {
        "orders": orders,
    }
    return render(request, 'orders_list.html', context=context)

def order_detail(request, order_id):
    order = next((order for order in orders if order['id'] == order_id), None)
    if order is None:
        return render(request, "order_not_found.html", {"order_id": order_id}, status=404)

    context = {
        "order": order,
    }

    return render(request, 'order_detail.html', context=context)
