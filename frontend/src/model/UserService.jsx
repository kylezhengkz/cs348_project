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
        console.log("EXT: ", ext);

        const res = await this.apiTool.post(ext, kwargs);

        return res.data;
    }

    async login(username, password) {
        const kwargs = {
            "username": username,
            "password": password
        }

        let ext = "/login";
        console.log("EXT: ", ext);

        const res = await this.apiTool.post(ext, kwargs);
        
        return res.data;
    }
}

export const userService = new UserService(apiTool);
