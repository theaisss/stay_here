from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    age: Optional[int]
    user_img: Optional[str]
    phone_number: Optional[str]
    user_role: str = 'client'
    city_id: Optional[int]

class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    age: Optional[int]
    user_img: Optional[str]
    phone_number: Optional[str]
    user_role: str
    is_active: bool
    is_verified: bool
    register_date: date
    city_id: Optional[int]

    class Config:
        from_attributes = True

class UserLoginSchema(BaseModel):
    username: str
    password: str


class RefreshTokenInputSchema(BaseModel):
    user_id: int
    token: str
    expires_at: datetime

class RefreshTokenOutSchema(BaseModel):
    id: int
    user_id: int
    token: str
    created_date: datetime
    expires_at: datetime
    is_revoked: bool

    class Config:
        from_attributes = True


class CountryInputSchema(BaseModel):
    country_name: str
    country_code: str

class CountryOutSchema(BaseModel):
    id: int
    country_name: str
    country_code: str

    class Config:
        from_attributes = True


class CityInputSchema(BaseModel):
    city_name: str
    city_image: Optional[str]
    country_id: int

class CityOutSchema(BaseModel):
    id: int
    city_name: str
    city_image: Optional[str]
    country_id: int

    class Config:
        from_attributes = True



class AmenityInputSchema(BaseModel):
    amenity_name: str
    amenity_icon: Optional[str]

class AmenityOutSchema(BaseModel):
    id: int
    amenity_name: str
    amenity_icon: Optional[str]

    class Config:
        from_attributes = True


class HotelInputSchema(BaseModel):
    hotel_name: str
    description: str
    stars: Optional[int]
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]
    city_id: int
    street: str
    postal_code: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    owner_id: Optional[int]

class HotelOutSchema(BaseModel):
    id: int
    hotel_name: str
    description: str
    stars: Optional[int]
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]
    is_active: bool
    created_at: datetime
    city_id: int
    street: str
    postal_code: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    owner_id: Optional[int]

    class Config:
        from_attributes = True


class HotelImageInputSchema(BaseModel):
    hotel_id: int
    image_url: str
    is_main: bool = False
    caption: Optional[str]

class HotelImageOutSchema(BaseModel):
    id: int
    hotel_id: int
    image_url: str
    is_main: bool
    caption: Optional[str]

    class Config:
        from_attributes = True


class HotelPolicyInputSchema(BaseModel):
    hotel_id: int
    check_in_time: Optional[str]
    check_out_time: Optional[str]
    pets_allowed: bool = False
    smoking_allowed: bool = False
    children_allowed: bool = True
    cancellation_policy: Optional[str]

class HotelPolicyOutSchema(BaseModel):
    id: int
    hotel_id: int
    check_in_time: Optional[str]
    check_out_time: Optional[str]
    pets_allowed: bool
    smoking_allowed: bool
    children_allowed: bool
    cancellation_policy: Optional[str]

    class Config:
        from_attributes = True

class RoomInputSchema(BaseModel):
    hotel_id: int
    room_number: Optional[str]
    room_type: str = 'single'
    description: str
    price_per_night: Decimal
    capacity: int = 2
    area_sqm: Optional[float] = None
    floor: Optional[int] = None
    is_available: bool = True
    has_balcony: bool = False
    has_sea_view: bool = False

class RoomOutSchema(BaseModel):
    id: int
    hotel_id: int
    room_number: Optional[str]
    room_type: str
    description: str
    price_per_night: Decimal
    capacity: int
    area_sqm: Optional[float] = None
    floor: Optional[int] = None
    is_available: bool
    has_balcony: bool
    has_sea_view: bool

    class Config:
        from_attributes = True



class RoomImageInputSchema(BaseModel):
    room_id: int
    image_url: str
    is_main: bool = False

class RoomImageOutSchema(BaseModel):
    id: int
    room_id: int
    image_url: str
    is_main: bool

    class Config:
        from_attributes = True


class BookingInputSchema(BaseModel):
    user_id: int
    hotel_id: int
    room_id: int
    check_in: date
    check_out: date
    guests_count: int = 1
    total_price: Decimal
    status: str = 'pending'
    special_requests: Optional[str]

class BookingOutSchema(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    room_id: int
    check_in: date
    check_out: date
    guests_count: int
    total_price: Decimal
    status: str
    special_requests: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaymentInputSchema(BaseModel):
    booking_id: int
    amount: Decimal
    currency: str = 'USD'
    method: str = 'card'
    status: str = 'unpaid'
    transaction_id: Optional[str]
    paid_at: Optional[datetime]

class PaymentOutSchema(BaseModel):
    id: int
    booking_id: int
    amount: Decimal
    currency: str
    method: str
    status: str
    transaction_id: Optional[str]
    paid_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True



class ReviewInputSchema(BaseModel):
    user_id: int
    hotel_id: int
    rating: int
    comment: str
    cleanliness: Optional[int]
    comfort: Optional[int]
    location: Optional[int]
    service: Optional[int]

class ReviewOutSchema(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    rating: int
    comment: str
    cleanliness: Optional[int]
    comfort: Optional[int]
    location: Optional[int]
    service: Optional[int]
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class WishlistInputSchema(BaseModel):
    user_id: int
    hotel_id: int

class WishlistOutSchema(BaseModel):
    id: int
    user_id: int
    hotel_id: int
    created_at: datetime

    class Config:
        from_attributes = True