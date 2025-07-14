# from .data import orders, services, masters
from .models import Order, Master, Service, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.context_processors import menu_items
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db.models import Q, Count, Sum
from django.shortcuts import get_object_or_404
from .forms import OrderForm
from django.http import JsonResponse

def about(request):
    # Здесь можно добавить логику для страницы "О нас"
    return render(request, 'about.html')

# def landing(request):
# # главная страница
#     masters = Master.objects.filter(is_active=True).prefetch_related('services')
#     reviews = Review.objects.filter(is_published=True).select_related('master')[:6]
#     context = {
#         'masters': masters,
#         'reviews': reviews,
#     }
#     return render(request, 'landing.html', context)
def landing(request):
    show_all = request.GET.get('show_all', False)
    all_reviews = Review.objects.filter(is_published=True).select_related('master')
    
    # Всегда считаем общее количество ОТДЕЛЬНО от среза
    total_reviews = all_reviews.count()
    reviews = all_reviews[:6] if not show_all else all_reviews
    
    context = {
        'masters': Master.objects.filter(is_active=True),
        'reviews': reviews,
        'show_all': show_all,
        'total_reviews': total_reviews,  # Добавляем в контекст
    }
    return render(request, 'landing.html', context)

def thanks(request):
    # Спасибо за заявку!
    return render(request, 'thanks.html')

@login_required # Декоратор проверяет, что пользователь авторизован
def orders_list(request):
    search_query = request.GET.get('q', '')
    search_fields = request.GET.getlist("search_fields", ["client_name"])
    orders = Order.objects.prefetch_related("services").order_by("-date_created")

    if search_query:
        q_objects = Q()
        if "client_name" in search_fields:
            q_objects |= Q(client_name__icontains=search_query)
        if "phone" in search_fields:
            q_objects |= Q(phone__icontains=search_query)
        if "comment" in search_fields:
            q_objects |= Q(comment__icontains=search_query)

        orders = orders.filter(q_objects)

    context = {
        "orders": orders,
        "search_query": search_query,
        "search_fields": search_fields,
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

def services_list(request):
    services = Service.objects.all()
    context = {"services": services}
    return render(request, "services.html", context=context)

def create_order(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == "POST":
        form = OrderForm(request.POST, service=service)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            order.services.add(service)
            return redirect("thanks")
    else:
        form = OrderForm(initial={'service': service}, service=service)
    
    return render(request, "create_order.html", 
        {"form": form,
        "service": service
        })