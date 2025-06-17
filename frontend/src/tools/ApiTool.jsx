import axios from "axios";


export class APITool {
    constructor(baseURL) {
        this._apiInstance = axios.create({ baseURL });
    }

    static addURLQuerySep(ext, apiVars) {
        for (const apiVar of apiVars) {
            if (apiVar == null || apiVar == undefined) {
                return ext;
            }
        }

        return `${ext}?`;
    }

    static getQueryKVP(key, val) {
        return (val == null || val == undefined) ? "" : `${key}=${val}`;
    }

    async get(apiExt) {
        const res = await this._apiInstance.get(`${apiExt}`);
        return res;
    }
}


export const apiTool = new APITool(process.env.REACT_APP_API_URL);