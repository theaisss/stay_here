from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer, String, Enum, Date, ForeignKey, Text,
    Boolean, DateTime, Float, Numeric, Table, Column
)
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date, datetime

class RoleChoices(str, PyEnum):
    client = 'client'
    owner  = 'owner'
    admin  = 'admin'


class RoomTypeChoices(str, PyEnum):
    single    = 'single'
    double    = 'double'
    twin      = 'twin'
    suite     = 'suite'
    family    = 'family'
    deluxe    = 'deluxe'
    penthouse = 'penthouse'
    economy   = 'economy'


class BookingStatusChoices(str, PyEnum):
    pending   = 'pending'
    confirmed = 'confirmed'
    cancelled = 'cancelled'
    completed = 'completed'


class PaymentStatusChoices(str, PyEnum):
    unpaid    = 'unpaid'
    paid      = 'paid'
    refunded  = 'refunded'
    failed    = 'failed'


class PaymentMethodChoices(str, PyEnum):
    card         = 'card'
    cash         = 'cash'
    bank_transfer = 'bank_transfer'
    online       = 'online'




hotel_amenity = Table(
    'hotel_amenity',
    Base.metadata,
    Column('hotel_id',   ForeignKey('hotel.id'),   primary_key=True),
    Column('amenity_id', ForeignKey('amenity.id'), primary_key=True),
)

class UserProfile(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    user_img: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    user_role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.client)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    register_date : Mapped[date] = mapped_column(Date, default=date.today)

    city_id: Mapped[Optional[int]] = mapped_column(ForeignKey('city.id'), nullable=True)

    city: Mapped[Optional['City']]          = relationship('City', back_populates='users')
    reviews: Mapped[List['Review']]             = relationship('Review', back_populates='user',
                                                                       cascade='all, delete-orphan')
    bookings: Mapped[List['Booking']]            = relationship('Booking', back_populates='user',
                                                                       cascade='all, delete-orphan')
    refresh_tokens: Mapped[List['RefreshToken']]       = relationship('RefreshToken', back_populates='user',
                                                                       cascade='all, delete-orphan')
    wishlist: Mapped[List['Wishlist']]            = relationship('Wishlist', back_populates='user',
                                                                       cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token: Mapped[str] = mapped_column(String, unique=True)
    created_date : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='refresh_tokens')


class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_name : Mapped[str] = mapped_column(String(80), unique=True)
    country_code : Mapped[str] = mapped_column(String(3), unique=True)   # e.g. "KG", "US"

    cities: Mapped[List['City']] = relationship('City', back_populates='country')


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_name: Mapped[str] = mapped_column(String(80), unique=True)
    city_image : Mapped[Optional[str]] = mapped_column(String, nullable=True)
    country_id : Mapped[int] = mapped_column(ForeignKey('country.id'))

    country: Mapped['Country'] = relationship('Country', back_populates='cities')
    hotels : Mapped[List['Hotel']]   = relationship('Hotel', back_populates='city')
    users: Mapped[List['UserProfile']] = relationship('UserProfile', back_populates='city')



class Amenity(Base):

    __tablename__ = 'amenity'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    amenity_name : Mapped[str] = mapped_column(String(50), unique=True)
    amenity_icon : Mapped[Optional[str]] = mapped_column(String, nullable=True)

    hotels: Mapped[List['Hotel']] = relationship('Hotel', secondary=hotel_amenity, back_populates='amenities')


class Hotel(Base):
    __tablename__ = 'hotel'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_name: Mapped[str] = mapped_column(String(100))
    description : Mapped[str] = mapped_column(Text)
    stars: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)   # 1–5
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    street: Mapped[str] = mapped_column(String(100))
    postal_code : Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), nullable=True)

    city: Mapped['City'] = relationship('City', back_populates='hotels')
    amenities : Mapped[List['Amenity']]     = relationship('Amenity', secondary=hotel_amenity, back_populates='hotels')
    images: Mapped[List['HotelImage']]  = relationship('HotelImage', back_populates='hotel',
                                                            cascade='all, delete-orphan')
    rooms: Mapped[List['Room']]        = relationship('Room', back_populates='hotel',
                                                            cascade='all, delete-orphan')
    reviews: Mapped[List['Review']]      = relationship('Review', back_populates='hotel',
                                                            cascade='all, delete-orphan')
    bookings: Mapped[List['Booking']]     = relationship('Booking', back_populates='hotel',
                                                            cascade='all, delete-orphan')
    policies: Mapped[List['HotelPolicy']] = relationship('HotelPolicy', back_populates='hotel',
                                                            cascade='all, delete-orphan')
    wishlists : Mapped[List['Wishlist']]    = relationship('Wishlist', back_populates='hotel',
                                                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Hotel {self.hotel_name}>'


class HotelImage(Base):
    __tablename__ = 'hotel_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    image_url : Mapped[str] = mapped_column(String)
    is_main: Mapped[bool] = mapped_column(Boolean, default=False)   # главная фотка
    caption: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)

    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='images')


class HotelPolicy(Base):
    __tablename__ = 'hotel_policy'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    check_in_time: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    check_out_time : Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    pets_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    smoking_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    children_allowed: Mapped[bool] = mapped_column(Boolean, default=True)
    cancellation_policy: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='policies')


class Room(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    room_number : Mapped[Optional[str]]      = mapped_column(String(10), nullable=True)
    room_type: Mapped[RoomTypeChoices] = mapped_column(Enum(RoomTypeChoices), default=RoomTypeChoices.single)
    description : Mapped[str] = mapped_column(Text)
    price_per_night: Mapped[float] = mapped_column(Numeric(10, 2))
    capacity: Mapped[int] = mapped_column(Integer, default=2)        # max guests
    area_sqm: Mapped[Optional[float]]   = mapped_column(Float, nullable=True)      # площадь м²
    floor: Mapped[Optional[int]]     = mapped_column(Integer, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    has_balcony : Mapped[bool] = mapped_column(Boolean, default=False)
    has_sea_view: Mapped[bool] = mapped_column(Boolean, default=False)
    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='rooms')
    images: Mapped[List['RoomImage']]  = relationship('RoomImage', back_populates='room',
                                                         cascade='all, delete-orphan')
    bookings: Mapped[List['Booking']]    = relationship('Booking', back_populates='room',
                                                         cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Room {self.room_number} | {self.room_type}>'


class RoomImage(Base):
    __tablename__ = 'room_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    image_url : Mapped[str] = mapped_column(String)
    is_main: Mapped[bool] = mapped_column(Boolean, default=False)

    room: Mapped['Room'] = relationship('Room', back_populates='images')


class Booking(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    check_in: Mapped[date] = mapped_column(Date)
    check_out: Mapped[date] = mapped_column(Date)
    guests_count : Mapped[int] = mapped_column(Integer, default=1)
    total_price: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[BookingStatusChoices] = mapped_column(Enum(BookingStatusChoices),
                                                                  default=BookingStatusChoices.pending)
    special_requests: Mapped[Optional[str]]      = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow,
                                                                  onupdate=datetime.utcnow)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='bookings')
    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='bookings')
    room: Mapped['Room'] = relationship('Room', back_populates='bookings')
    payment: Mapped[Optional['Payment']] = relationship('Payment', back_populates='booking',
                                                         uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Booking #{self.id} | {self.status}>'


class Payment(Base):
    __tablename__ = 'payment'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey('booking.id'), unique=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(3), default='USD')
    method: Mapped[PaymentMethodChoices] = mapped_column(Enum(PaymentMethodChoices),
                                                                      default=PaymentMethodChoices.card)
    status: Mapped[PaymentStatusChoices] = mapped_column(Enum(PaymentStatusChoices),
                                                                      default=PaymentStatusChoices.unpaid)
    transaction_id : Mapped[Optional[str]]          = mapped_column(String, nullable=True)  # от платёжки
    paid_at: Mapped[Optional[datetime]]     = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    booking: Mapped['Booking'] = relationship('Booking', back_populates='payment')



class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    rating: Mapped[int] = mapped_column(Integer)          # 1–10
    comment: Mapped[str] = mapped_column(Text)
    cleanliness: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # sub-ratings
    comfort: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    location: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    service: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='reviews')
    user : Mapped['UserProfile'] = relationship('UserProfile', back_populates='reviews')


class Wishlist(Base):
    __tablename__ = 'wishlist'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user : Mapped['UserProfile'] = relationship('UserProfile', back_populates='wishlist')
    hotel: Mapped['Hotel'] = relationship('Hotel', back_populates='wishlists')