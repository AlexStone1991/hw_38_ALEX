from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta
from .models import Service, Master, Review, Order


class AppointmentDateFilter(admin.SimpleListFilter):
    title = 'Дата записи'
    parameter_name = 'appointment_date'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Сегодня'),
            ('week', 'На неделе'),
            ('month', 'В этом месяце'),
        )
    
    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'today':
            today = now.date()
            return queryset.filter(appointment_date__date=today)
        if self.value() == 'tomorrow':
            tomorrow = now.date() + timedelta(days=1)
            return queryset.filter(appointment_date__date=tomorrow)
        if self.value() == 'this_week':
            start_week = now.date() - timedelta(days=now.weekday())
            end_week = start_week + timedelta(days=6)
            return queryset.filter(appointment_date__date__range=[start_week, end_week])

# Фильтр по сумме заказа
class TotalPriceFilter(admin.SimpleListFilter):
    title = 'Сумма заказа'
    parameter_name = 'total_price'

    def lookups(self, request, model_admin):
        return (
            ('<1000', 'До 1000 руб'),
            ('1000-3000', '1000-3000 руб'),
            ('>3000', 'Более 3000 руб'),
        )

    def queryset(self, request, queryset):
        queryset = queryset.annotate(total=Sum('services__price'))
        if self.value() == '<1000':
            return queryset.filter(total__lt=1000)
        if self.value() == '1000-3000':
            return queryset.filter(total__range=(1000, 3000))
        if self.value() == '>3000':
            return queryset.filter(total__gt=3000)

# Инлайн для услуг мастера
class MasterServicesInline(admin.TabularInline):
    model = Master.services.through
    extra = 0
    verbose_name = "Доступная услуга"
    verbose_name_plural = "Доступные услуги"
    autocomplete_fields = ['service']

# Инлайн для отзывов
class ReviewsInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['created_at']
    fields = ['client_name', 'master', 'rating', 'is_published', 'created_at']

# Инлайн для услуг в заказе
class OrderServicesInline(admin.TabularInline):
    model = Order.services.through
    extra = 1
    verbose_name = "Услуга в заказе"
    autocomplete_fields = ['service']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'masters_count']
    search_fields = ['name']
    list_filter = ['is_popular']
    
    def masters_count(self, obj):
        return obj.masters.count()
    masters_count.short_description = "Мастеров"

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'experience', 'active_status', 'services_list', 'services_count']
    list_filter = ['is_active']
    search_fields = ['name', 'phone']
    inlines = [MasterServicesInline, ReviewsInline]

    def services_list(self, obj):
        return ", ".join(s.name for s in obj.services.all()[:3])

    services_list.short_description = "Услуги"

    def active_status(self, obj):
        return "✅" if obj.is_active else "❌"

    active_status.short_description = "Активен"

    def services_count(self, obj):
        return obj.services.count()

    services_count.short_description = "Кол-во услуг"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_name', 'phone', 'appointment_date', 
                'status', 'get_total_price', 'master_info']
    list_filter = ['status', TotalPriceFilter, 'master', AppointmentDateFilter]
    list_editable = ['status']
    search_fields = ['client_name', 'phone']
    inlines = [OrderServicesInline]
    exclude = ['services']
    readonly_fields = ['date_created', 'date_updated']
    actions = ['mark_completed', 'mark_confirmed', 'mark_canceled', 'mark_in_progress']
    
    def get_total_price(self, obj):
        return sum(s.price for s in obj.services.all())
    get_total_price.short_description = "Сумма"
    
    def status_badge(self, obj):
        colors = {
            'new': 'orange',
            'confirmed': 'blue',
            'completed': 'green',
            'canceled': 'red'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 10px">{}</span>',
            colors[obj.status],
            obj.get_status_display()
        )
    status_badge.short_description = "Статус"
    
    def master_info(self, obj):
        if obj.master:
            return format_html('<a href="/admin/core/master/{}/change/">{}</a>',
                            obj.master.id, obj.master.name)
        return "-"
    master_info.short_description = "Мастер"
    
    @admin.action(description="Отметить как завершенные")
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
    
    @admin.action(description="Подтвердить выбранные")
    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description="Отменить выбранные")
    def mark_canceled(self, request, queryset):
        queryset.update(status='canceled')

    @admin.action(description="Пометить 'В работе'")
    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'master', 'rating_stars', "created_at",'is_published']
    list_filter = ['rating', 'is_published', 'master']
    search_fields = ['client_name', 'text']
    list_editable = ("is_published",)
    
    @admin.display(description='Рейтинг')
    def rating_stars(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)