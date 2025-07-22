select *
from "Building"
WHERE TRUE
    AND (%(buildingName)s IS NULL OR "buildingName" ILIKE %(buildingName)s)
    AND (%(addressLine1)s IS NULL OR "addressLine1" ILIKE %(addressLine1)s)
    AND (%(addressLine2)s IS NULL OR "addressLine2" ILIKE %(addressLine2)s)
    AND (%(city)s IS NULL OR "city" ILIKE %(city)s)
    AND (%(province)s IS NULL OR "province" ILIKE %(province)s)
    AND (%(country)s IS NULL OR "country" ILIKE %(country)s)
    AND (%(postalCode)s IS NULL OR "postalCode" ILIKE %(postalCode)s)
;