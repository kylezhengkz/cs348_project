import axios from "axios";


export class APITool {
    constructor(baseURL) {
        this._apiInstance = axios.create({ baseURL });
    }

    static hasQueryVars(apiVars) {
        for (const apiVar of apiVars) {
            if (apiVar !== null && apiVar !== undefined) {
                return true;
            }
        }

        return false;
    }

    static addURLQuerySep(ext, apiVars) {
        const queryVarsAvailable = APITool.hasQueryVars(apiVars);
        return queryVarsAvailable ? `${ext}?` : ext;
    }

    static getQueryKVPStr(key, val) {
        return (val === null || val === undefined) ? "" : `${key}=${val}`;
    }

    static getQueryKwargsStr(kwargs) {
        const result = [];
        for (const key in kwargs) {
            const queryKVPStr = APITool.getQueryKVPStr(key, kwargs[key]);
            if (queryKVPStr !== "") {
                result.push(queryKVPStr);
            }
        }

        return result.join("&");
    }

    async get(apiExt) {
        const res = await this._apiInstance.get(`${apiExt}`);
        return res;
    }
}


export const apiTool = new APITool(process.env.REACT_APP_API_URL);