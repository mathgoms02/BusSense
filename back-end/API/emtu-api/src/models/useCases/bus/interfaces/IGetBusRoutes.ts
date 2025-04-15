
import BusRoute from './../../../busRoute';
export interface IGetBusRoutesUseCase {
  execute(origin: string, destination: string): Promise<BusRoute[]>
}
