import { VehicleDto } from "../../dtos/vehicleDto";

export interface IVehicleDatasource {
  getByPrefix(prefix: string[]): Promise<VehicleDto[]>;
};