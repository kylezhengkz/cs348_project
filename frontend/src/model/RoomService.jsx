import { BaseAPIService } from "./BaseAPIService";
import { APITool, apiTool } from "../tools/ApiTool";


export class RoomService extends BaseAPIService {
    async getAvailable(roomName, minCapacity, maxCapacity, 
                 startTimeStr, endTimeStr) {
        
        const kwargs = {
            "room_name": roomName,
            "min_capacity": minCapacity,
            "max_capacity": maxCapacity,
            "start_time": startTimeStr,
            "end_time": endTimeStr
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

    async deleteRoom(roomID) {
        const kwargs = {
            "roomID": roomID
        }

        let ext = "/deleteRoom";
        console.log("EXT: ", ext);

        const res = await this.apiTool.post(ext, kwargs);

        console.log(res.data)

        return res.data;
    }
}


export const roomService = new RoomService(apiTool);