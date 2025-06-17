import { BaseAPIService } from "./BaseAPIService";
import { APITool, apiTool } from "../tools/ApiTool";


export class RoomService extends BaseAPIService {
    async getAvailable(roomName, minCapacity, maxCapacity, 
                 startTimeStr, endTimeStr) {
        
        const kvps = {
            "room_name": roomName,
            "minCapacity": minCapacity,
            "maxCapacity": maxCapacity,
            "startTimeStr": startTimeStr,
            "endTimeStr": endTimeStr
        }

        let ext = APITool.addURLQuerySep("/viewAvailableRooms", Object.values(kvps));
        for (const key in kvps) {
            ext += APITool.getQueryKVP(key, kvps[key]);
        }

        console.log("EXT: ", ext);

        const res = await this.apiTool.get(ext);
        return res.data;
    }
}


export const roomService = new RoomService(apiTool);