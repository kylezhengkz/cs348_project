import { BaseAPIService } from "./BaseAPIService";
import { APITool, apiTool } from "../tools/ApiTool";


export class RoomService extends BaseAPIService {
    async getRoomsByBuildingID(buildingID) {
        let ext = `/viewRoomsByBuildingID?building_id=${buildingID}&db_operation=filter`
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

        const res = await this.apiTool.get(ext);
        return res.data;
    }

    async addRoom(roomName, capacity, buildingID, userID) {
        const kwargs = {
            "roomName": roomName,
            "capacity": capacity,
            "buildingID": buildingID,
            "userID": userID
        }

        let ext = "/addRoom";
        const res = await this.apiTool.post(ext, kwargs);
        return res.data;
    }

    async deleteRoom(roomID, userID) {
        const kwargs = {
            "roomID": roomID,
            "userID": userID,
        }

        let ext = "/deleteRoom";
        const res = await this.apiTool.post(ext, kwargs);

        console.log(res.data)

        return res.data;
    }

    async editRoom(roomID, roomName, capacity, userID) {
        const kwargs = {
            "roomID": roomID,
            "roomName": roomName,
            "capacity": capacity,
            "userID": userID
        }

        let ext = "/editRoom";
        const res = await this.apiTool.post(ext, kwargs);
        return res.data;
    }
}


export const roomService = new RoomService(apiTool);