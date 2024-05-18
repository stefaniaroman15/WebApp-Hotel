import json
from django.core.management.base import BaseCommand
from hotelApp.models import Hotel, Room

class Command(BaseCommand):
    help = 'Load hotel data from JSON file'

    def handle(self, *args, **kwargs):
        with open('path_to_your_json_file.json', 'r') as file:
            data = json.load(file)

        for hotel_data in data['hotels']:
            hotel, created = Hotel.objects.get_or_create(
                name=hotel_data['name'],
                latitude=hotel_data['latitude'],
                longitude=hotel_data['longitude'],
            )
            for room_data in hotel_data['rooms']:
                Room.objects.get_or_create(
                    hotel=hotel,
                    room_number=room_data['room_number'],
                    type=room_data['type'],
                    price=room_data['price'],
                    is_available=room_data['is_available'],
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded hotel data'))
