# hotels/management/commands/populate_hotels.py

import json
from django.core.management.base import BaseCommand
from hotelApp.models import Hotel, Room

class Command(BaseCommand):
    help = 'Populates the database with hotels data from a JSON file'

    def handle(self, *args, **kwargs):
        with open('hotels.json', 'r') as file:
            hotels_data = json.load(file)
            for hotel_data in hotels_data:
                hotel = Hotel.objects.create(
                    id=hotel_data['id'],
                    name=hotel_data['name'],
                    latitude=hotel_data['latitude'],
                    longitude=hotel_data['longitude']
                )
                rooms_data = hotel_data['rooms']
                for room_data in rooms_data:
                    Room.objects.create(
                        hotel=hotel,
                        room_number=room_data['roomNumber'],
                        type=room_data['type'],
                        price=room_data['price'],
                        is_available=room_data['isAvailable']
                    )
        self.stdout.write(self.style.SUCCESS('Hotels data has been successfully populated'))
