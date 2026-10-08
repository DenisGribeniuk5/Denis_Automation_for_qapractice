from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingDates(BaseModel):
    model_config = ConfigDict(extra="forbid")

    checkin: date
    checkout: date


class Booking(BaseModel):
    model_config = ConfigDict(extra="forbid")

    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str | None = None


class CreatedBooking(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bookingid: int
    booking: Booking


class BookingId(BaseModel):
    bookingid: int


class Token(BaseModel):
    token: str
