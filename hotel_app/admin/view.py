from hotel_app.database.models import (
    UserProfile, RefreshToken, Country, City, Amenity,
    Hotel, HotelImage, HotelPolicy, Room, RoomImage,
    Booking, Payment, Review, Wishlist
)
from sqladmin import ModelView

class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [
        UserProfile.id,
        UserProfile.first_name,
        UserProfile.last_name,
        UserProfile.username,
        UserProfile.email,
        UserProfile.user_role,
        UserProfile.is_active
    ]

class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [
        RefreshToken.id,
        RefreshToken.user_id,
        RefreshToken.token,
        RefreshToken.created_date,
        RefreshToken.expires_at,
        RefreshToken.is_revoked
    ]

class CountryAdmin(ModelView, model=Country):
    column_list = [
        Country.id,
        Country.country_name,
        Country.country_code
    ]

class CityAdmin(ModelView, model=City):
    column_list = [
        City.id,
        City.city_name,
        City.country_id,
        City.city_image
    ]

class AmenityAdmin(ModelView, model=Amenity):
    column_list = [
        Amenity.id,
        Amenity.amenity_name,
        Amenity.amenity_icon
    ]

class HotelAdmin(ModelView, model=Hotel):
    column_list = [
        Hotel.id,
        Hotel.hotel_name,
        Hotel.city_id,
        Hotel.stars,
        Hotel.street,
        Hotel.owner_id,
        Hotel.is_active
    ]

class HotelImageAdmin(ModelView, model=HotelImage):
    column_list = [
        HotelImage.id,
        HotelImage.hotel_id,
        HotelImage.image_url,
        HotelImage.is_main
    ]

class HotelPolicyAdmin(ModelView, model=HotelPolicy):
    column_list = [
        HotelPolicy.id,
        HotelPolicy.hotel_id,
        HotelPolicy.check_in_time,
        HotelPolicy.check_out_time,
        HotelPolicy.pets_allowed
    ]

class RoomAdmin(ModelView, model=Room):
    column_list = [
        Room.id,
        Room.room_number,
        Room.hotel_id,
        Room.room_type,
        Room.price_per_night,
        Room.is_available
    ]

class RoomImageAdmin(ModelView, model=RoomImage):
    column_list = [
        RoomImage.id,
        RoomImage.room_id,
        RoomImage.image_url,
        RoomImage.is_main
    ]

class BookingAdmin(ModelView, model=Booking):
    column_list = [
        Booking.id,
        Booking.user_id,
        Booking.hotel_id,
        Booking.room_id,
        Booking.check_in,
        Booking.check_out,
        Booking.status,
        Booking.total_price
    ]

class PaymentAdmin(ModelView, model=Payment):
    column_list = [
        Payment.id,
        Payment.booking_id,
        Payment.amount,
        Payment.currency,
        Payment.method,
        Payment.status
    ]

class ReviewAdmin(ModelView, model=Review):
    column_list = [
        Review.id,
        Review.user_id,
        Review.hotel_id,
        Review.rating,
        Review.comment,
        Review.is_approved,
        Review.created_at
    ]

class WishlistAdmin(ModelView, model=Wishlist):
    column_list = [
        Wishlist.id,
        Wishlist.user_id,
        Wishlist.hotel_id,
        Wishlist.created_at
    ]