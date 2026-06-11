from fastapi import FastAPI
import uvicorn
from hotel_app.api import (users, city, hotel, hotel_image, hotel_policy, review, rooms,
                           room_image, booking, country, amenity, payment, wishlist, auth)
from hotel_app.admin.setup import setup_admin

hotel_app = FastAPI()

hotel_app.include_router(auth.auth_router)
hotel_app.include_router(users.user_router)
hotel_app.include_router(country.country_router)
hotel_app.include_router(city.city_router)
hotel_app.include_router(hotel.hotel_router)
hotel_app.include_router(hotel_image.hotel_image_router)
hotel_app.include_router(hotel_policy.policy_router)
hotel_app.include_router(amenity.amenity_router)
hotel_app.include_router(rooms.room_router)
hotel_app.include_router(room_image.room_image_router)
hotel_app.include_router(booking.booking_router)
hotel_app.include_router(payment.payment_router)
hotel_app.include_router(review.review_router)
hotel_app.include_router(wishlist.wishlist_router)

setup_admin(hotel_app)

if __name__ == '__main__':
    uvicorn.run('main:hotel_app', host='127.0.0.1', port=8000, reload=True)