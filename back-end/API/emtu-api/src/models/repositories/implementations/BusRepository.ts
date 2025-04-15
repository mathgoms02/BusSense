import { AxiosResponse } from "axios";
import IBusDataSource from "../../../database/interfaces/busDataSource";
import { IBusExternal } from "../../../external/interfaces/busExternal";
import BusRoute from "../../busRoute";
import { IBusRepository } from "../IBusRepository";

export default class BusRepository implements IBusRepository {
  busDataSource: IBusDataSource;
  busExternal: IBusExternal;
  constructor(busDataSource: IBusDataSource, busExternal: IBusExternal){
    this.busDataSource = busDataSource;
    this.busExternal = busExternal;
  }
  async getRoute(origin: string, destination: string): Promise<BusRoute[]> {
    try {
      if(!origin || !destination)
        return null;
      return await this.busDataSource.getRoute(origin, destination);
    } catch (error) {
      throw(error);
    }
  }

  async getLines(route: BusRoute[]): Promise<AxiosResponse<any, any>[]> {
    if(route == null) return null;
    try {
      return await this.busExternal.getLinesDetails(route);
    } catch (error) {
      throw new Error(error);
    }
  }
}