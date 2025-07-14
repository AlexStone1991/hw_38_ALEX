from django.core.management.base import BaseCommand
from core.models import Master, Service, Review
import random

class Command(BaseCommand):
    help = 'Load initial data for barbershop'

    def handle(self, *args, **options):
        # Очистка старых данных
        Master.objects.all().delete()
        Service.objects.all().delete()
        Review.objects.all().delete()

        # Данные мастеров
        masters_data = [
            {"name": "Алексей Петров", "experience": 12, "phone": "+79123456789", "address": "ул. Ленина, 10", "is_active": True},
            {"name": "Иван Иванов", "experience": 8, "phone": "+79123456788", "address": "ул. Пушкина, 15", "is_active": True},
            {"name": "Мария Сидорова", "experience": 10, "phone": "+79123456787", "address": "ул. Гоголя, 20", "is_active": True},
            {"name": "Анна Кузнецова", "experience": 15, "phone": "+79123456786", "address": "ул. Толстого, 25", "is_active": True},
            {"name": "Дмитрий Смирнов", "experience": 9, "phone": "+79123456785", "address": "ул. Чехова, 30", "is_active": True},
            {"name": "Ольга Васильева", "experience": 7, "phone": "+79123456784", "address": "ул. Достоевского, 35", "is_active": True},
        ]

        # Данные услуг
        services_data = [
            {"name": "Классическая стрижка", "price": 1500.00, "duration": 45, "description": "Аккуратная стрижка", "is_popular": True},
            {"name": "Бритье опасной бритвой", "price": 2000.00, "duration": 30, "description": "Классическое бритье", "is_popular": True},
            {"name": "Стрижка машинкой", "price": 1200.00, "duration": 40, "description": "Современная стрижка машинкой", "is_popular": False},
            {"name": "Окрашивание", "price": 3500.00, "duration": 90, "description": "Окрашивание волос", "is_popular": True},
            {"name": "Укладка", "price": 1800.00, "duration": 25, "description": "Стильная укладка", "is_popular": False},
            {"name": "Коррекция бороды", "price": 2500.00, "duration": 60, "description": "Коррекция формы бороды", "is_popular": True},
            {"name": "Стрижка бороды", "price": 2200.00, "duration": 50, "description": "Уход за бородой", "is_popular": True},
            {"name": "Комплексный уход", "price": 3000.00, "duration": 75, "description": "Полный уход за волосами", "is_popular": False},
            {"name": "Экспресс-стрижка", "price": 1000.00, "duration": 20, "description": "Быстрая стрижка", "is_popular": True},
            {"name": "Вечерняя укладка", "price": 5000.00, "duration": 120, "description": "Укладка для вечернего выхода", "is_popular": True}
        ]

        # Создание услуг
        services = []
        for service in services_data:
            services.append(Service.objects.create(**service))

        # Создание мастеров
        masters = []
        for master in masters_data:
            new_master = Master.objects.create(**master)
            # Каждый мастер получает случайные 3-5 услуг
            new_master.services.set(random.sample(services, k=random.randint(3, 5)))
            masters.append(new_master)

        # Данные отзывов
        reviews_data = [
            {"text": "Отличный мастер! Очень доволен результатом.", "client_name": "Алексей", "rating": 5},
            {"text": "Профессионал своего дела. Рекомендую всем!", "client_name": "Иван", "rating": 5},
            {"text": "Очень вежливый и аккуратный. Спасибо за отличную стрижку!", "client_name": "Сергей", "rating": 4},
            {"text": "Приятно удивлен качеством. Буду приходить еще.", "client_name": "Антон", "rating": 5},
            {"text": "Спасибо за отличную работу! Все очень понравилось.", "client_name": "Дмитрий", "rating": 5},
            {"text": "Не очень понравилось. Мастер немного торопился.", "client_name": "Олег", "rating": 3},
            {"text": "Все хорошо, но можно было бы и лучше.", "client_name": "Михаил", "rating": 4},
            {"text": "Не совсем то, что я ожидал. Возможно, в следующий раз выберу другого мастера.", "client_name": "Владимир", "rating": 2},
            {"text": "Отличный сервис! Очень доволен.", "client_name": "Андрей", "rating": 5},
            {"text": "Спасибо за отличную стрижку! Все супер.", "client_name": "Николай", "rating": 5}
        ]

        # Создание отзывов
        for review in reviews_data:
            Review.objects.create(
                text=review["text"],
                client_name=review["client_name"],
                rating=review["rating"],
                master=random.choice(masters)
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))
