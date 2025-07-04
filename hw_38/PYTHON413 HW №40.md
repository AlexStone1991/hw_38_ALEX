---
project: "[[Академия TOP]]"
journal: "[[PYTHON413]]"
tags:
  - PYTHON413
date: 2025-06-28
type:
  - home work
hw_num: 40
topic: В этом задании вам необходимо создать модели для базы данных проекта "Барбершоп". Вы создадите модели для заказов, мастеров, услуг и отзывов, настроите миграции и зарегистрируете модели в админке Django. Кроме того, потребуется установить и подключить пакет shell plus, создать суперпользователя и убедиться в корректной работе приложения с тестовыми данными (не менее 3–5 записей в каждой таблице).
hw_theme:
  - django
  - orm
  - shell_plus
  - django-extensions
  - Миграции
st_group: python 413
links:
  - "[[PYTHON411 HW №23]]"
---
# Домашнее задание 📃

**Создание моделей для БД и настройка административной панели проекта "Барбершоп".**

## Краткое содержание

В этом задании вам необходимо создать модели для базы данных проекта "Барбершоп". Вы создадите модели для заказов, мастеров, услуг и отзывов, настроите миграции и зарегистрируете модели в админке Django. Кроме того, потребуется установить и подключить пакет shell plus, создать суперпользователя и убедиться в корректной работе приложения с тестовыми данными (не менее 3–5 записей в каждой таблице).

Обратите внимание, что миграции должны присутствовать в сданной работе и размещаться на GitHub. А вот файл базы данных, не стоит размещать на GitHub. Только в личном кабинете в архиве!

### Технологии: 🦾

- Python  
- Django  
- ORM Django  
- Миграции  
- shell_plus (django-extensions)  
- Git (с обязательными не менее 5 коммитами)  
- Административная панель Django

## Задание 👷‍♂️

### 1. Создание моделей и настройка миграций

Создайте в приложении  `core` следующие модели:

- **Order (Заказ)**
  - `client_name`: CharField (max_length=100, verbose_name="Имя клиента")
  - `phone`: CharField (max_length=20, verbose_name="Телефон")
  - `comment`: TextField (blank=True, verbose_name="Комментарий")
  - `status`: CharField (max_length=50, choices=STATUS_CHOICES, default="not_approved", verbose_name="Статус")
  - `date_created`: DateTimeField (auto_now_add=True, verbose_name="Дата создания")
  - `date_updated`: DateTimeField (auto_now=True, verbose_name="Дата обновления")
  - `master`: ForeignKey (на мастера, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Мастер")
  - `services`: ManyToManyField (с услугами, related_name="orders", verbose_name="Услуги")
  - `appointment_date`: DateTimeField (verbose_name="Дата и время записи")

- **Master (Мастер)**
  - `name`: CharField (max_length=150, verbose_name="Имя")
  - `photo`: ImageField (upload_to="masters/", blank=True, verbose_name="Фотография")
  - `phone`: CharField (max_length=20, verbose_name="Телефон")
  - `address`: CharField (max_length=255, verbose_name="Адрес")
  - `experience`: PositiveIntegerField (verbose_name="Стаж работы", help_text="Опыт работы в годах")
  - `services`: ManyToManyField (с услугами, related_name="masters", verbose_name="Услуги")
  - `is_active`: BooleanField (default=True, verbose_name="Активен")

- **Service (Услуга)**
  - `name`: CharField (max_length=200, verbose_name="Название")
  - `description`: TextField (blank=True, verbose_name="Описание")
  - `price`: DecimalField (max_digits=10, decimal_places=2, verbose_name="Цена")
  - `duration`: PositiveIntegerField (verbose_name="Длительность", help_text="Время выполнения в минутах")
  - `is_popular`: BooleanField (default=False, verbose_name="Популярная услуга")
  - `image`: ImageField (upload_to="services/", blank=True, verbose_name="Изображение")

- **Review (Отзыв)**
  - `text`: TextField (verbose_name="Текст отзыва")
  - `client_name`: CharField (max_length=100, blank=True, verbose_name="Имя клиента")
  - `master`: ForeignKey (на мастера, on_delete=models.CASCADE, verbose_name="Мастер")
  - `photo`: ImageField (upload_to="reviews/", blank=True, null=True, verbose_name="Фотография")
  - `created_at`: DateTimeField (auto_now_add=True, verbose_name="Дата создания")
  - `rating`: PositiveSmallIntegerField (с валидаторами MinValueValidator(1) и MaxValueValidator(5), verbose_name="Оценка") (Или через CHOICES)
  - `is_published`: BooleanField (default=True, verbose_name="Опубликован")

>[!info]
>
>#### Рекомендации по работе с моделями
>
>- Используйте аннотации типов и подробные docstring для каждого класса и метода.  
>- При создании полей обращайте внимание на ограничения (max_length, null, blank и т.п.).  
>- Не забывайте про связные поля – для M2M и ForeignKey правильно указывайте аргументы `related_name` и `on_delete`.

После создания моделей выполните следующие шаги:

- Сгенерируйте миграции с помощью команды:  
  `python manage.py makemigrations`
- Примените миграции:  
  `python manage.py migrate`
- Проверьте, что в каждой таблице данные создаются, сделайте не менее 3–5 тестовых записей.

### 2. Версионирование и коммиты

Требования к системе контроля версий:

- Сделайте не менее 5 коммитов. Префикс каждого коммита должен быть вида `hw_<номер>: сообщение коммита` (например, `hw_XX: добавлены модели Order, Master, Service, Review`).
- **Важно:** На GitHub не должны попадать файлы БД – они должны быть исключены через `.gitignore` (например, sqlite3 файл).

>[!warning]
>
>#### Основные требования к коммитам
>
>- **Не менее 5 коммитов:** каждый значимый этап должен фиксироваться отдельным коммитом.
>- **Формат сообщений коммитов:** `hw_<номер>: краткое описание проделанной работы`.

### 3. Обеспечение работы через shell_plus и создание суперпользователя

- Установите пакет `django-extensions` через pip (или добавьте его в зависимости через Poetry).  
- В файле `settings.py` подключите его, добавив в `INSTALLED_APPS`:
  - `'django_extensions'`
- Используйте команду:  
  `python manage.py shell_plus`  
  для удобного доступа к моделям и тестированию.
- Создайте суперпользователя с помощью команды:  
  `python manage.py createsuperuser`
- После чего подключите созданные модели в административной панели Django, зарегистрировав их в файле `admin.py` вашего приложения.

>[!warning]
>
>#### Ключевые моменты при настройке администратора
>
>- Зарегистрируйте все модели (`Order`, `Master`, `Service` и `Review`) для их отображения в админке.
>- Проверьте корректную работу админки, зайдя под суперпользователем и убедившись, что все данные отображаются верно.

### 4. Тестовые данные и проверка работы

- Заполните каждую таблицу (заказы, мастера, услуги, отзывы) не менее чем 3–5 записями. Это можно сделать как через `Django shell`, так и через админку.
- Проверьте, что связи между моделями (`M2M` и `ForeignKey`) работают корректно, а все ограничения полей соблюдаются.

### Таблица моделей и их полей

| Модель    | Поля                                                                                                | Описание                                                     |
| --------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `Order`   | client_name, phone, comment, status, date_created, date_updated, master, services, appointment_date | Информация о заказе клиента с привязками к мастеру и услугам |
| `Master`  | name, photo, phone, address, experience, services, is_active                                        | Данные о мастерах барбершопа                                 |
| `Service` | name, description, price, duration, is_popular, image                                               | Описание и параметры услуги                                  |
| `Review`  | text, client_name, master, photo, created_at, rating, is_published                                  | Отзывы клиентов о работе мастеров и качестве услуг           |

## Критерии оценки 👌

1. **Модели и миграции: 6 баллов**
   - Модели созданы с нужными полями и ограничениями
   - Миграции сгенерированы и применены
   - В каждой таблице 3-5 тестовых записей
   - Файлы БД исключены через .gitignore

2. **Административная панель: 3 балла**
   - Суперпользователь создан
   - Модели зарегистрированы в админке
   - Админка корректно отображает данные

3. **Тестирование и shell_plus: 2 балла**
   - Установлен и работает django-extensions
   - Проверены связи между моделями
   - Созданы тестовые данные через shell_plus (**Скриншот приложен**)

4. **Кодирование и документация: 1 балл**
   - Код соответствует PEP 8
   - Сделано не менее 5 коммитов с префиксом hw_23:
   - В архиве присутствуют все необходимые файлы
