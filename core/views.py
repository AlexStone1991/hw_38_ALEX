from django.shortcuts import render
from .data import orders, services, masters
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect


def about(request):
    # Здесь можно добавить логику для страницы "О нас"
    return render(request, 'about.html')

def get_services_with_masters():
    # Создаем словарь, где ключом будет название услуги, а значением - список мастеров, которые ее выполняют
    return [
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

def all_services(request):
    # список услуг шаблон
    context = {
        'services_with_masters': get_services_with_masters(),
    }
    return render(request, 'services.html', context=context)

def all_masters(request):
    # список мастеров шаблон
    context = {
        'masters': masters,
    }
    return render(request, 'masters.html', context=context)

def appointment(request):
    # форма записи
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        service = request.POST.get('service')
        master = request.POST.get('master')
        date = request.POST.get('date')
        messages.success(request, f'Заявка на услугу "{service}" отправлена!')
        return redirect('thanks')
    context = {
        'services': services,
        'masters': masters,
    }
    return render(request, 'appointment.html', context=context)

def landing(request):
# главная страница
    context = {
        'masters': masters,
        'services_with_masters': get_services_with_masters(),
    }
    return render(request, 'landing.html', context)

def thanks(request):
    # Спасибо за заявку!
    return render(request, 'thanks.html')

@login_required # Декоратор проверяет, что пользователь авторизован
def orders_list(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Для просмотра заказов необходимо авторизоваться')
        return redirect('landing')
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
