from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Hotel, Room, Reservation, Feedback
from .utils import haversine
from django.http import HttpResponseForbidden
# Home page view
def index(request):
    return render(request, 'index.html')



def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.rooms.filter(is_available=True)
    return render(request, 'room_list.html', {'hotel': hotel, 'rooms': rooms})

# View to list all hotels
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel_list.html', {'hotels': hotels})

# View to display hotel details and available rooms
def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.rooms.filter(is_available=True)
    return render(request, 'hotel_detail.html', {'hotel': hotel, 'rooms': rooms})

# View to handle room booking
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        user_name = request.POST.get('user_name')

        reservation = Reservation.objects.create(
            room=room,
            user_name=user_name,
            check_in=check_in,
            check_out=check_out,
            is_active=True,
        )

        room.is_available = False
        room.save()

        return redirect('reservation_detail', reservation.id)

    return render(request, 'book_room.html', {'room': room})

# View to display reservation details
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservation_detail.html', {'reservation': reservation})

# View to handle feedback submission
def leave_feedback(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        services_rating = request.POST.get('services_rating')
        cleanliness_rating = request.POST.get('cleanliness_rating')
        comments = request.POST.get('comments')

        Feedback.objects.create(
            reservation=reservation,
            services_rating=services_rating,
            cleanliness_rating=cleanliness_rating,
            comments=comments,
        )

        return redirect('reservation_detail', reservation.id)

    return render(request, 'leave_feedback.html', {'reservation': reservation})

# View to find nearby hotels based on user's location
def find_nearby_hotels(request):
    user_lat = float(request.GET.get('latitude'))
    user_lon = float(request.GET.get('longitude'))
    radius = float(request.GET.get('radius'))

    nearby_hotels = []
    for hotel in Hotel.objects.all():
        distance = haversine(user_lon, user_lat, hotel.longitude, hotel.latitude)
        if distance <= radius:
            nearby_hotels.append(hotel)

    return render(request, 'hotel_list.html', {'hotels': nearby_hotels})


def view_hotels(request):
    hotels = Hotel.objects.all()
    return render(request, 'view_hotels.html', {'hotels': hotels})


from django.shortcuts import render
import json


def display_hotels(request):
    with open('hotelApp/management/commands/hotels.json', 'r') as f:
        data = json.load(f)

    return render(request, 'hotel_list.html', {'hotels': data})
def reserve_room(request):
    if request.method == 'POST':
        hotel_id = request.POST.get('hotel_id')
        room_number = request.POST.get('room_number')

        # Folosește hotel_id și room_number pentru a identifica camera în baza de date
        room = Room.objects.filter(hotel__id=hotel_id, room_number=room_number).first()

        if room:
            user_name = request.POST.get('user_name')
            phone_number = request.POST.get('phone_number')
            check_in = request.POST.get('check_in')
            check_out = request.POST.get('check_out')

            reservation = Reservation.objects.create(
                room=room,
                user_name=user_name,
                phone_number=phone_number,
                check_in=check_in,
                check_out=check_out,
                is_active=True,
            )

            room.is_available = False
            room.save()

            # Redirecționează către pagina de detalii a rezervării
            return redirect('reservation_detail', reservation.id)

    return render(request, 'book_room.html')


def leave_feedback(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    # Verificăm dacă rezervarea este activă
    if not reservation.is_active:
        return HttpResponseForbidden("You can't leave feedback for an inactive reservation.")

    if request.method == 'POST':
        overall_rating = request.POST.get('overall_rating')
        comments = request.POST.get('comments')

        # Creăm feedback-ul și îl asociem rezervării
        feedback = Feedback.objects.create(
            reservation=reservation,
            overall_rating=overall_rating,
            comments=comments
        )

        # Redirecționăm utilizatorul către detalii despre rezervare sau altă pagină
        return redirect('reservation_detail', reservation_id=reservation.id)

    # Returnăm un template pentru formularul de feedback
    return render(request, 'leave_feedback.html', {'reservation': reservation})
def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservation_list.html', {'reservations': reservations})