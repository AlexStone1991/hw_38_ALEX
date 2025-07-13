from django.contrib import admin
from .models import Master, Order, Service, Review
from django.db.models import Q, Count, Sum, QuerySet

# Фильтр для OrderAdmin по общей сумме заказа (из кода преподавателя)
class TotalOrderPrice(admin.SimpleListFilter):
    title = "По общей сумме заказа"
    parameter_name = "total_order_price"

    def lookups(self, request, model_admin):
        return (
            ("one_thousend", "До тысячи"),
            ("three_thousend", "До трех тысяч"),
            ("five_thousend", "До пяти тысяч"),
            ("up_five_thousend", "Свыше пяти тысяч"),
        )
    
    def queryset(self, request, queryset):
        queryset = queryset.annotate(total_price_agg=Sum("services__price"))
        
        if self.value() == "one_thousend":
            return queryset.filter(total_price_agg__lt=1000)
        if self.value() == "three_thousend":
            return queryset.filter(total_price_agg__gte=1000, total_price_agg__lt=3000)
        if self.value() == "five_thousend":
            return queryset.filter(total_price_agg__gte=3000, total_price_agg__lt=5000)
        if self.value() == "up_five_thousend":
            return queryset.filter(total_price_agg__gte=5000)
        
        return queryset

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Исправлено: client_name вместо name + добавлены улучшения
    list_display = (
        "id",
        "client_name",  # Исправленное поле
        "phone",
        "formatted_master",  # Кастомное отображение мастера
        "date_created",
        "appointment_date",
        "status",
        "total_price",
        "total_income",
        "formatted_services",  # Кастомное отображение услуг
    )
    
    search_fields = ("client_name", "phone", "status", "master__name")  # Добавлен поиск по мастеру
    list_filter = ("status", "master", "services", TotalOrderPrice)
    list_per_page = 5
    list_display_links = ("phone", "client_name")
    list_editable = ("status",)
    readonly_fields = ("date_created", "date_updated")
    date_hierarchy = "date_created"  # Добавлена временная шкала
    filter_horizontal = ("services",)  # Удобный выбор услуг

    actions = ("mark_completed", "mark_canceled", "mark_new", "mark_confirmed")

    # Кастомные методы отображения (новые)
    @admin.display(description="Мастер")
    def formatted_master(self, obj):
        return obj.master.name if obj.master else "Не назначен"

    @admin.display(description="Услуги")
    def formatted_services(self, obj):
        return ", ".join([s.name for s in obj.services.all()])

    # Методы из кода преподавателя
    @admin.action(description="Отметить как завершенные")
    def mark_completed(self, request, queryset):
        queryset.update(status="completed")

    @admin.action(description="Отметить как отмененная")
    def mark_canceled(self, request, queryset):
        queryset.update(status="canceled")

    @admin.action(description="Отметить как новая")
    def mark_new(self, request, queryset):
        queryset.update(status="new")

    @admin.action(description="Отметить как подтвержденная")
    def mark_confirmed(self, request, queryset):
        queryset.update(status="confirmed")

    @admin.display(description="Общая сумма")
    def total_price(self, obj):
        return sum(service.price for service in obj.services.all())

    @admin.display(description="Выручка")
    def total_income(self, obj):
        orders = Order.objects.filter(
            phone=obj.phone, 
            status="completed"
        ).prefetch_related("services")
        return sum(service.price for order in orders for service in order.services.all())

# Улучшенные админ-классы для других моделей
@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "experience", "is_active", "service_count")
    list_filter = ("is_active", "services")
    search_fields = ("name", "phone")
    filter_horizontal = ("services",)  # Удобное управление услугами
    
    @admin.display(description="Кол-во услуг")
    def service_count(self, obj):
        return obj.services.count()

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration", "is_popular", "master_count")
    list_filter = ("is_popular",)
    search_fields = ("name",)
    ordering = ("name",)
    
    @admin.display(description="Мастеров")
    def master_count(self, obj):
        return obj.masters.count()

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("client_name", "master", "rating_stars", "created_at", "is_published")
    list_filter = ("rating", "is_published", "master")
    search_fields = ("client_name", "master__name")
    date_hierarchy = "created_at"
    
    @admin.display(description="Рейтинг")
    def rating_stars(self, obj):
        return "★" * obj.rating + "☆" * (5 - obj.rating)