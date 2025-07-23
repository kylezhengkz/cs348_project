import { BaseAPIService } from "./BaseAPIService"
import { apiTool } from "../tools/ApiTool";

export class DashBoardService extends BaseAPIService {
    async getDashboardMetrics(userId) {
        const ext = `/getDashboardMetrics?userId=${userId}`;
        const res = await this.apiTool.get(ext);
        return res;
    }

    async getBookingFrequency(userId, startDateTime, endDateTime, queryLimit) {
        const kwargs = {
            "userId": userId,
            "startDateTime": startDateTime,
            "endDateTime": endDateTime,
            "queryLimit": queryLimit
        }

        const ext = "/getBookingFrequency";
        const res = await this.apiTool.post(ext, kwargs);
        return res.data;
    }
}

export const dashBoardService = new DashBoardService(apiTool);