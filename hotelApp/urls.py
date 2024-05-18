from django.urls import path
from . import views

urlpatterns = [
    path('hotels/', views.display_hotels, name='hotel_list'),
    path('room_list/<int:hotel_id>/', views.room_list, name='room_list'),  # Verifică dacă funcția room_list este definită în views.py
    path('reserve_room/', views.reserve_room, name='reserve_room'),
    path('', views.index, name='index'),
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('book_room/<int:room_id>/', views.book_room, name='book_room'),
    path('reservation/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('leave_feedback/<int:reservation_id>/', views.leave_feedback, name='leave_feedback'),
    path('find_nearby_hotels/', views.find_nearby_hotels, name='find_nearby_hotels'),
    path('reservations/', views.reservation_list, name='reservation_list'),
]


