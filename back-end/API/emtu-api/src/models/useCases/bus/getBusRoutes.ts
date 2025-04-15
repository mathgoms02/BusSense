import BusRoute from "../../busRoute";
import { IBusRepository } from "../../repositories/IBusRepository";
import { IGetBusRoutesUseCase } from "./interfaces/IGetBusRoutes";

class GetBusRoutesUseCase implements IGetBusRoutesUseCase {
  busRepository : IBusRepository;
  constructor (busRepository: IBusRepository){
    this.busRepository = busRepository;
  }

  async execute(origin: string, destination: string): Promise<BusRoute[]> {
    try {
      if(!origin || !destination) return null;
      origin = origin.normalize('NFD').replace(/[\u0300-\u036f]/g, "");
      destination = destination.normalize('NFD').replace(/[\u0300-\u036f]/g, "");
      return await this.busRepository.getRoute(origin, destination);
    } catch (error) {
      throw  new Error(error);
    }
  }
  
}

export { GetBusRoutesUseCase }