import { BaseAPIService } from "./BaseAPIService";
import { apiTool } from "../tools/ApiTool";

export class UserService extends BaseAPIService {
    async signup(username, email, password) {
        const kwargs = {
            "username": username,
            "email": email,
            "password": password,
        }

        let ext = "/signup";
        const res = await this.apiTool.post(ext, kwargs);
        return res.data;
    }

    async login(username, password) {
        const kwargs = {
            "username": username,
            "password": password
        }

        let ext = "/login";
        const res = await this.apiTool.post(ext, kwargs);
        
        return res.data;
    }

    async viewAdminLog(userID) {
        const kwargs = {
            "userID": userID
        }

        let ext = "/viewAdminLog";
        const res = await this.apiTool.post(ext, kwargs);
        
        return res.data;
    }

    async updateUsername(userId, newUsername) {
        const kwargs = {
            "userId": userId,
            "newUsername": newUsername
        }

        const ext = "/updateUsername";
        const res = await this.apiTool.post(ext, kwargs);
        return res.data;
    }

    async updatePassword(userId, oldPassword, newPassword) {
        const kwargs = {
            "userId": userId,
            "oldPassword": oldPassword,
            "newPassword": newPassword
        }
    
        const ext = "/updatePassword";
        const res = await this.apiTool.post(ext, kwargs);
        return res.data;
    }    
}

export const userService = new UserService(apiTool);
