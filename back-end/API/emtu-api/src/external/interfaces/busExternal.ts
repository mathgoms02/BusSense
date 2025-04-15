
import { AxiosResponse } from 'axios';
import BusRoute from './../../models/busRoute';
export interface IBusExternal {
  getLinesDetails(busRoutes: BusRoute[]): Promise<AxiosResponse<any, any>[]>;
}