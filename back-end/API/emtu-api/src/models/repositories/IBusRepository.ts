import { AxiosResponse } from "axios";
import BusRoute from "../busRoute";

interface IBusRepository {
  getRoute(origin: string, destination: string) : Promise<BusRoute[]>;
  getLines(route : BusRoute[]): Promise<AxiosResponse<any, any>[]>;
};

export { IBusRepository };