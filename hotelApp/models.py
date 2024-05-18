from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('suite', 'Suite Room'),
        ('matrimonial', 'Matrimonial Room'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.IntegerField()
    type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.FloatField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_number} - {self.hotel.name}"

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user_name} - {self.room}"

class Feedback(models.Model):
    reservation = models.OneToOneField('Reservation', on_delete=models.CASCADE, related_name='feedback')
    overall_rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"Feedback for {self.reservation}"