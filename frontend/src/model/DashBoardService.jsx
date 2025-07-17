import { BaseAPIService } from "./BaseAPIService"
import { apiTool } from "../tools/ApiTool";

export class DashBoardService extends BaseAPIService {
    async getDashboardMetrics(userId) {
        const ext = `/getDashboardMetrics?userId=${userId}`;
        const res = await this.apiTool.get(ext);
        return res;
    }
}

export const dashBoardService = new DashBoardService(apiTool);