# from .data import orders, services, masters
from .models import Order, Master, Service, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.context_processors import menu_items
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db.models import Q, Count, Sum, Prefetch
from django.shortcuts import get_object_or_404
from .forms import OrderForm, ReviewForm
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime

def about(request):
    # Здесь можно добавить логику для страницы "О нас"
    return render(request, 'about.html')

def landing(request):
    show_all = request.GET.get('show_all', False)
    all_reviews = Review.objects.filter(is_published=True).select_related('master')
    
    # Всегда считаем общее количество ОТДЕЛЬНО от среза
    total_reviews = all_reviews.count()
    reviews = all_reviews[:6] if not show_all else all_reviews
    masters = Master.objects.prefetch_related('services').annotate(num_services=Count('services'))
    context = {
        'masters': masters,
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
    masters = Master.objects.all()
    min_date = timezone.now().strftime('%Y-%m-%dT%H:%M') 
    context = {
        "services": services,
        "masters": masters,
        "form": OrderForm(),
        "min_date": min_date
    }
    return render(request, "services.html", context=context)

def create_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш отзыв отправлен на модерацию!")
            return redirect("thanks")
    else:
        form = ReviewForm()

    return render(request, "create_review.html", {"form": form})

def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, "Заявка успешко отправлена!")
            return redirect("thanks")
    else:
        form = OrderForm()
    return render(request, "create_order.html", {"form": form})

def master_services_api(request, master_id):
    master = get_object_or_404(Master, id=master_id)
    services = master.services.all().values('id', 'name', 'price')  # Добавляем price
    return JsonResponse({
        'services': list(services) 
    })

def service_masters_api(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    masters = service.masters.all().values('id', 'name')  # Получаем мастеров, предоставляющих эту услугу
    return JsonResponse({
        'masters': list(masters)
    })

def master_detail(request, master_id):
    master = get_object_or_404(
        Master.objects.prefetch_related('services', 'review_set'),
        id=master_id,
        is_active=True
    )
    
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.master = master
            review.save()
            return redirect('master_detail', master_id=master.id)
    else:
        review_form = ReviewForm(initial={'master': master})
    
    context = {
        'master': master,
        'review_form': review_form,
    }
    return render(request, 'master_detail.html', context)

def your_view(request):
    min_date = timezone.now().strftime('%Y-%m-%dT%H:%M')
    context = {
        'min_date': min_date,
    }
    return render(request, 'your_template.html', context)