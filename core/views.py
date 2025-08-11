from .models import Order, Master, Service, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.context_processors import menu_items
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db.models import Q, Count, Sum, Prefetch
from django.shortcuts import get_object_or_404
from .forms import OrderForm, ReviewForm
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views import View
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    TemplateView,
)

class AboutView(TemplateView):
    template_name = 'about.html'

class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show_all = self.request.GET.get('show_all', False)
        all_reviews = Review.objects.filter(is_published=True).select_related('master')

        total_reviews = all_reviews.count()
        reviews = all_reviews[:6] if not show_all else all_reviews
        masters = Master.objects.prefetch_related('services').annotate(num_services=Count('services'))

        context.update({
            'masters': masters,
            'reviews': reviews,
            'show_all': show_all,
            'total_reviews': total_reviews,
        })
        return context


class ThanksView(TemplateView):
    template_name = 'thanks.html'

@method_decorator(login_required, name='dispatch')
class OrdersListView(ListView):
    model = Order
    template_name = 'orders_list.html'
    context_object_name = 'orders'
    ordering = ['-date_created']

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("services")
        search_query = self.request.GET.get('q', '')
        search_fields = self.request.GET.getlist("search_fields", ["client_name"])

        if search_query:
            q_objects = Q()
            if "client_name" in search_fields:
                q_objects |= Q(client_name__icontains=search_query)
            if "phone" in search_fields:
                q_objects |= Q(phone__icontains=search_query)
            if "comment" in search_fields:
                q_objects |= Q(comment__icontains=search_query)
            queryset = queryset.filter(q_objects)

        return queryset

@method_decorator(login_required, name='dispatch')
class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return super().get_queryset().prefetch_related("services").select_related("master").annotate(total_price=Sum('services__price'))

class ServicesListView(TemplateView):
    template_name = 'services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "services": Service.objects.all(),
            "masters": Master.objects.all(),
            "form": OrderForm(),
            "min_date": timezone.now().strftime('%Y-%m-%dT%H:%M')
        })
        return context

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'create_review.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, "Ваш отзыв отправлен на модерацию!")
        return super().form_valid(form)

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'create_order.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, "Заявка успешно отправлена!")
        return super().form_valid(form)

class MasterServicesAPIView(View):
    def get(self, request, master_id):
        master = get_object_or_404(Master, id=master_id)
        services = master.services.all().values('id', 'name', 'price')
        return JsonResponse({'services': list(services)})

class ServiceMastersAPIView(View):
    def get(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
        masters = service.masters.all().values('id', 'name')
        return JsonResponse({'masters': list(masters)})

class MasterDetailView(DetailView):
    model = Master
    template_name = 'master_detail.html'
    context_object_name = 'master'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Master.objects.prefetch_related('services', 'review_set'),
            id=self.kwargs['master_id'],
            is_active=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm(initial={'master': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        review_form = ReviewForm(request.POST, request.FILES)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.master = self.object
            review.save()
            return redirect('master_detail', master_id=self.object.id)

        context = self.get_context_data(**kwargs)
        context['review_form'] = review_form
        return self.render_to_response(context)
