import BusRoute from "../../models/busRoute";

export default interface IBusDataSource {
  getRoute(origin: string, destination: string): Promise<BusRoute[]>
}