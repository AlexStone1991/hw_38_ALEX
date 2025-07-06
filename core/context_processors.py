from .models import Service, Master

def menu_items(request):
    services = Service.objects.all()
    masters = Master.objects.all()
    return {
        'services': services,
        'masters': masters,
    }