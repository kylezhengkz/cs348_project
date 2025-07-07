import { BaseAPIService } from "./BaseAPIService";
import { APITool, apiTool } from "../tools/ApiTool";

export class UserService extends BaseAPIService {
    async signup(username, email, password) {
        const kwargs = {
            "username": username,
            "email": email,
            "password": password,
        }

        let ext = "/signup";
        const queryVarsAvailable = APITool.hasQueryVars(Object.values(kwargs));

        console.log("EXT: ", ext);

        const res = await this.apiTool.post(ext, kwargs);

        return res.data;
    }
}

export const userService = new UserService(apiTool);
