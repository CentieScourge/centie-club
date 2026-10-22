from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.home, name='home'),
    path('laws/', views.laws, name='laws'),
    path('business/', views.business_list, name='business'),
    # path('map/', views.map_view, name='map'),
    path('feedback/', views.feedback, name='feedback'),
    path('meeting/', views.meeting_form, name='meeting'),
    path('employees/', views.employees, name='employees'),
    path('notifications/', views.notifications_api, name='notifications_api'),
]
