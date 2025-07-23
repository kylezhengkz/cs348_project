import { BaseAPIService } from "./BaseAPIService";
import { APITool, apiTool } from "../tools/ApiTool";


export class BuildingService extends BaseAPIService {
    async fetchBuildings(buildingName, addressLine1, addressLine2, 
                 city, province, country, postalCode) {
        
        const kwargs = {
            "buildingName": buildingName,
            "addressLine1": addressLine1,
            "addressLine2": addressLine2,
            "city": city,
            "province": province,
            "country": country,
            "postalCode": postalCode
        }

        let ext = "/viewBuildings";
        const queryVarsAvailable = APITool.hasQueryVars(Object.values(kwargs));
        
        if (queryVarsAvailable) {
            kwargs["db_operation"] = "filter";
            ext += "?";            
        }

        ext += APITool.getQueryKwargsStr(kwargs);
        const res = await this.apiTool.get(ext);
        return res.data;
    }
}


export const buildingService = new BuildingService(apiTool);