import { VehicleDto } from "../../../dtos/vehicleDto";
import { DEFAULT_CID } from "../../const/cidConsts";
import { IVehicleRepository } from "../IVehiclesRepository";
import { IVehicleDatasource } from './../../../database/interfaces/vehiclesDatasource';

export class VehicleRepository implements IVehicleRepository {
  vehicleDatasource: IVehicleDatasource;

  constructor(vehicleDatasource: IVehicleDatasource) {
    this.vehicleDatasource = vehicleDatasource;
  }

  async getByPrefix(prefixArray: string[]): Promise<VehicleDto[]> {
    if (!prefixArray.length) return null;

    let vehicles = await this.vehicleDatasource.getByPrefix(prefixArray);
    const notFoundPrefixes = prefixArray.filter(prefix =>
      !vehicles.some(vehicle => vehicle.prefix === prefix)
    );

    if (notFoundPrefixes && notFoundPrefixes.length > 0 ) {
      notFoundPrefixes.forEach(prefix => {
        vehicles.push({
          'id': null,
          'prefix': prefix,
          'name': '',
          'group': DEFAULT_CID,
        });
      });
    }
    return vehicles;
  }

}