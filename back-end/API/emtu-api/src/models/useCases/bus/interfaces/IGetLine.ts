import BusRoute from "../../../busRoute";

export interface IGetLine {
  execute(busRoute: BusRoute[],date:Date, hour: Date, originCity: string, destinyCity: string): Promise<object>
}