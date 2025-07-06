from enum import Enum


class ColNames(Enum):
    UserId = "userID"
    UserIdExists = "userID_exists"
    BuildingId = "buildingID"
    BuildingName = "buildingName"
    BuildingAddressLine1 = "addressLine1"
    BuildingAddressLine2 = "addressLine2"
    BuildingCity = "city"
    BuildingProvince = "province"
    BuildingCountry = "country"
    BuildingPostalCode = "postalCode"
    BuildingIdExists = "buildingID_exists"
    RoomId = "roomID"
    RoomIdExists = "roomID_exists"
    BookingId = "bookingID"
    BookingTime = "bookDateTime"
    BookingStartTime = "bookStartDateTime"
    BookingEndTime = "bookEndDateTime"
    BookingIdExists = "bookingID_exists"