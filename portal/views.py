from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import (
    Business, Employee, News, Document, Review, Meeting,
    PrivateOrg, SiteInfo, Notification
)


def home(request):
    news = News.objects.filter(published=True)[:10]
    total_business = Business.objects.count()
    free_business = Business.objects.filter(status='free').count()
    review_count = Review.objects.count()
    return render(request, 'portal/home.html', {
        'news_list': news,
        'total_business': total_business,
        'free_business': free_business,
        'review_count': review_count,
    })


def laws(request):
    documents = Document.objects.all()
    return render(request, 'portal/laws.html', {'documents': documents})


def business_list(request):
    businesses = Business.objects.all()
    status = request.GET.get('status')
    btype = request.GET.get('type')
    if status and status != 'all':
        businesses = businesses.filter(status=status)
    if btype and btype != 'all':
        businesses = businesses.filter(type=btype)
    orgs = PrivateOrg.objects.all()
    return render(request, 'portal/business.html', {
        'businesses': businesses,
        'orgs': orgs,
        'current_status': status or 'all',
        'current_type': btype or 'all',
    })


def map_view(request):
    return render(request, 'portal/map.html')


def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'Гражданин LS').strip() or 'Гражданин LS'
        text = request.POST.get('text', '').strip()
        if text:
            Review.objects.create(name=name, text=text)
            return redirect('portal:feedback')
    reviews = Review.objects.all()
    return render(request, 'portal/feedback.html', {'reviews': reviews})


def meeting_form(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        card_id = request.POST.get('card_id', '').strip()
        topic = request.POST.get('topic', '')
        custom = request.POST.get('custom_topic', '').strip()
        if name and phone and card_id and len(phone) == 10 and phone.isdigit():
            Meeting.objects.create(
                name=name, phone=phone, card_id=card_id,
                topic=topic, custom_topic=custom if topic == 'Другое' else ''
            )
            return redirect('portal:meeting')
    meetings = Meeting.objects.all() if request.user.is_authenticated and request.user.is_admin_role() else []
    return render(request, 'portal/meeting.html', {'meetings': meetings})


def employees(request):
    staff = Employee.objects.all()
    return render(request, 'portal/employees.html', {'employees': staff})


@login_required
def notifications_api(request):
    """JSON endpoint for live notifications polling."""
    qs = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:20]
    data = [{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'link': n.link,
        'created_at': n.created_at.isoformat(),
    } for n in qs]
    return JsonResponse({'notifications': data, 'count': qs.count()})
