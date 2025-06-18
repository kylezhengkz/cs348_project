import { BaseAPIService } from "./BaseAPIService";
import { APITool, apiTool } from "../tools/ApiTool";


export class RoomService extends BaseAPIService {
    async getAvailable(roomName, minCapacity, maxCapacity, 
                 startTimeStr, endTimeStr) {
        
        const kwargs = {
            "room_name": roomName,
            "minCapacity": minCapacity,
            "maxCapacity": maxCapacity,
            "startTimeStr": startTimeStr,
            "endTimeStr": endTimeStr
        }

        let ext = "/viewAvailableRooms";
        const queryVarsAvailable = APITool.hasQueryVars(Object.values(kwargs));

        if (queryVarsAvailable) {
            kwargs["db_operation"] = "filter";
            ext += "?";            
        }

        ext += APITool.getQueryKwargsStr(kwargs);
        console.log("EXT: ", ext);

        const res = await this.apiTool.get(ext);
        return res.data;
    }
}


export const roomService = new RoomService(apiTool);