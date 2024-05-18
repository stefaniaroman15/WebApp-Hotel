from django.contrib import admin
from django.urls import path, include
from hotelApp import views as hotel_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hotelapp/', include('hotelApp.urls')),
    path('', hotel_views.index, name='home'),  # Definește ruta pentru URL-ul rădăcină
]
