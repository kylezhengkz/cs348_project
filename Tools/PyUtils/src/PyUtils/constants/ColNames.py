from enum import Enum


class ColNames(Enum):
    UserId = "userID"
    BuildingId = "buildingID"
    BuildingName = "buildingName"
    BuildingAddressLine1 = "addressLine1"
    BuildingAddressLine2 = "addressLine2"
    BuildingCity = "city"
    BuildingProvince = "province"
    BuildingCountry = "country"
    BuildingPostalCode = "postalCode"
    RoomId = "roomID"
    BookingId = "bookingID"
    BookingTime = "bookDateTime"
    BookingStartTime = "bookStartDateTime"
    BookingEndTime = "bookEndDateTime"