from .models import SiteInfo

def site_context(request):
    return {
        'site_title': 'Мэрия Лос-Сантоса',
    }
