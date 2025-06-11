from enum import Enum

class ColNames(Enum):
    UserId = "userID"
    BuildingId = "buildingID"
    BuildingAddressLine2 = "addressLine1"
    BuildingProvince = "province"
    RoomId = "roomID"
    BookingId = "bookingID"
    BookingTime = "bookDateTime"
    BookingStartTime = "bookStartDateTime"
    BookingEndTime = "bookEndDateTime"