from fastapi import FastAPI
from sqladmin import Admin
from hotel_app.database.db import engine
from .view import (
    UserProfileAdmin, RefreshTokenAdmin, CountryAdmin, CityAdmin,
    AmenityAdmin, HotelAdmin, HotelImageAdmin, HotelPolicyAdmin,
    RoomAdmin, RoomImageAdmin, BookingAdmin, PaymentAdmin,
    ReviewAdmin, WishlistAdmin
)

def setup_admin(hotel_app: FastAPI):
    admin = Admin(hotel_app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(RefreshTokenAdmin)
    admin.add_view(CountryAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(AmenityAdmin)
    admin.add_view(HotelAdmin)
    admin.add_view(HotelImageAdmin)
    admin.add_view(HotelPolicyAdmin)
    admin.add_view(RoomAdmin)
    admin.add_view(RoomImageAdmin)
    admin.add_view(BookingAdmin)
    admin.add_view(PaymentAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(WishlistAdmin)