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
            {"name": "Мо Сизлак", "experience": 12, "phone": "+1234567890", "address": "Ул. Вечнозелёная, 742", "is_active": True},
            {"name": "Барни Гамбл", "experience": 8, "phone": "+1234567891", "address": "Ул. Пьяная, 1", "is_active": True},
            {"name": "Апу Нахасапимапетилон", "experience": 10, "phone": "+1234567892", "address": "Мини-маркет Kwik-E-Mart", "is_active": True},
            {"name": "Доктор Хибберт", "experience": 15, "phone": "+1234567893", "address": "Медцентр Спрингфилда", "is_active": True},
            {"name": "Шеф Виггам", "experience": 9, "phone": "+1234567894", "address": "Полицейский участок", "is_active": True},
            {"name": "Лиза Симпсон", "experience": 3, "phone": "+1234567895", "address": "Школа Спрингфилда", "is_active": True},
            {"name": "Клоун Красти", "experience": 7, "phone": "+1234567896", "address": "Театр Красти", "is_active": True},
            {"name": "Неду Фландерс", "experience": 5, "phone": "+1234567897", "address": "Дом по соседству", "is_active": True},
            {"name": "Великий Чумба", "experience": 20, "phone": "+1234567898", "address": "Цирк", "is_active": True},
            {"name": "Снейк", "experience": 6, "phone": "+1234567899", "address": "Тюрьма Спрингфилда", "is_active": False}
        ]

        # Данные услуг
        services_data = [
            {"name": "Классическая стрижка", "price": 1500, "duration": 45, "description": "Аккуратная стрижка в стиле Гомера Симпсона", "is_popular": True},
            {"name": "Бритьё опасной бритвой", "price": 2000, "duration": 30, "description": "Королевское бритьё как у мистера Бёрнса", "is_popular": True},
            {"name": "Детская стрижка", "price": 1200, "duration": 40, "description": "Стрижка для маленьких непосед как у Барта", "is_popular": False},
            {"name": "Окрашивание", "price": 3500, "duration": 90, "description": "Яркие цвета как у Мардж", "is_popular": True},
            {"name": "Укладка премиум", "price": 1800, "duration": 25, "description": "Стильная укладка как у Лизи", "is_popular": False},
            {"name": "Камуфляж лысины", "price": 2500, "duration": 60, "description": "Маскировка проплешин как у дяди Пита", "is_popular": True},
            {"name": "Бородатый стиль", "price": 2200, "duration": 50, "description": "Уход за бородой как у Мо", "is_popular": True},
            {"name": "Креативный авангард", "price": 3000, "duration": 75, "description": "Смелый стиль как у клоуна Красти", "is_popular": False},
            {"name": "Экспресс-стрижка", "price": 1000, "duration": 20, "description": "Быстро и качественно между кружками пива", "is_popular": True},
            {"name": "Полный образ", "price": 5000, "duration": 120, "description": "Комплексный уход как для звезды шоу-бизнеса", "is_popular": True}
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

        # Создание отзывов
        reviews_data = [
            {"text": "Отличный мастер!", "client_name": "Клиент 1", "rating": 5},
            {"text": "Очень доволен результатом.", "client_name": "Клиент 2", "rating": 4},
            {"text": "Профессионал своего дела.", "client_name": "Клиент 3", "rating": 5},
            {"text": "Спасибо за отличную стрижку!", "client_name": "Клиент 4", "rating": 4},
            {"text": "Рекомендую всем!", "client_name": "Клиент 5", "rating": 5},
            {"text": "Очень вежливый и аккуратный.", "client_name": "Клиент 6", "rating": 4},
            {"text": "Приятно удивлен качеством.", "client_name": "Клиент 7", "rating": 5},
            {"text": "Отличный сервис!", "client_name": "Клиент 8", "rating": 5},
            {"text": "Очень доволен.", "client_name": "Клиент 9", "rating": 4},
            {"text": "Спасибо за отличную работу!", "client_name": "Клиент 10", "rating": 5}
        ]

        for review in reviews_data:
            Review.objects.create(
                text=review["text"],
                client_name=review["client_name"],
                rating=review["rating"],
                master=random.choice(masters)
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))
