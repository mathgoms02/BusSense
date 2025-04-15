import { VehicleDto } from "../../dtos/vehicleDto";

export interface IVehicleRepository {
  getByPrefix(prefix: string[]): Promise<VehicleDto[]>;
};