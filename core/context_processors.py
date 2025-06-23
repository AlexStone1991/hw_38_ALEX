from .models import MenuItem

def menu_items(request):
    # Пример: получение элементов меню из базы данных
    items = MenuItem.objects.all()
    return {'menu_items': items}

