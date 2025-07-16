import { BaseAPIService } from "./BaseAPIService"
import { apiTool } from "../tools/ApiTool";


export class BookingService extends BaseAPIService {
    async bookRoom(userId, roomId, startDateTime, endDateTime, participants) {
        const kwargs = {
            "user_id": userId,
            "room_id": roomId,
            "start_time": startDateTime,
            "end_time": endDateTime,
            "participants": participants
        };

        let ext = "/bookRoom";

        const res = await this.apiTool.post(ext, kwargs);
        return res;
    }

    async cancelBooking(userId, bookingId) {
        const kwargs = {
            "booking_id": bookingId,
            "user_id": userId
        };

        let ext = "/cancelBooking";

        const res = await this.apiTool.post(ext, kwargs);
        return res;
    }

    async getFutureBookings(userId) {
        const ext = `/getFutureBookings?userId=${userId}`;
        const res = await this.apiTool.get(ext);
        return res;
    }

    async getBookingsAndCancellations(userId) {
        const ext = `/getBookingsAndCancellations?userId=${userId}`;
        const res = await this.apiTool.get(ext);
        return res;
    }
    async getDashboardMetrics(userId) {
        const ext = `/getDashboardMetrics?userId=${userId}`;
        const res = await this.apiTool.get(ext);
        return res;
    }
    
}


export const bookingService = new BookingService(apiTool);