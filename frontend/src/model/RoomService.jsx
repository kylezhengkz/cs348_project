import { BaseAPIService } from "./BaseAPIService";
import { APITool, apiTool } from "../tools/ApiTool";


export class RoomService extends BaseAPIService {
    async getRoomsByBuildingID(buildingID) {
        let ext = `/viewRoomsByBuildingID?building_id=${buildingID}&db_operation=filter`
        console.log("EXT: ", ext);

        const res = await this.apiTool.get(ext);
        return res.data;
    }

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

    async addRoom(roomName, capacity, buildingID) {
        const kwargs = {
            "roomName": roomName,
            "capacity": capacity,
            "buildingID": buildingID
        }

        let ext = "/addRoom";
        console.log("EXT: ", ext);
        console.log(kwargs)

        const res = await this.apiTool.post(ext, kwargs);

        console.log(res.data)

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

    async editRoom(roomID, roomName, capacity) {
        const kwargs = {
            "roomID": roomID,
            "roomName": roomName,
            "capacity": capacity
        }

        let ext = "/editRoom";
        console.log("EXT: ", ext);

        const res = await this.apiTool.post(ext, kwargs);
        console.log(res.data)
        return res.data;
    }
}


export const roomService = new RoomService(apiTool);