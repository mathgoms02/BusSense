
import { IVerifyAccessibility } from './interfaces/IVerifyAccessibility';
import { IVehicleRepository } from './../../repositories/IVehiclesRepository';
import { ICidsRepository } from '../../repositories/ICidsRepository';
import { VehicleDto, VehicleResponse } from '../../../dtos/vehicleDto';
import { CidsDto } from '../../../dtos/cidsDto';
import { DEFAULT_CID } from '../../const/cidConsts';

export class VerifyAccessibilityUseCase implements IVerifyAccessibility {
  vehiclesRepository: IVehicleRepository;
  cidsRepository: ICidsRepository;

  constructor(vehiclesRepository: IVehicleRepository, cidsRepository: ICidsRepository) {
    this.vehiclesRepository = vehiclesRepository;
    this.cidsRepository = cidsRepository;
  }

  async execute(prefix: string[], cid: number): Promise<VehicleResponse[]> {
    const vehiclesArray = await this.vehiclesRepository.getByPrefix(prefix);
    const cidObj = await this.cidsRepository.getById(cid);

    if (cidObj == null) return null;

    return this.setVehicleAccessibility(vehiclesArray, cidObj);

  }

  private setVehicleAccessibility(vehiclesArray: VehicleDto[], cidObj: CidsDto): VehicleResponse[] {
    let responseArray = [] as VehicleResponse[];
    if (!vehiclesArray || !(vehiclesArray.length > 0))
      vehiclesArray = [{ id: null, prefix: null, name: null, group: DEFAULT_CID }];

    vehiclesArray.forEach((vehicle) => {

      if (vehicle == null && cidObj.group == DEFAULT_CID) return responseArray.push(this.setVehicleObject(vehicle, true));

      if (vehicle && cidObj.group == vehicle.group) return responseArray.push(this.setVehicleObject(vehicle, true));

      return responseArray.push(this.setVehicleObject(vehicle, false));

    });

    return responseArray;
  };

  private setVehicleObject(vehicle: VehicleDto, accessibility: boolean): VehicleResponse {
    return {
      'id': vehicle.id,
      'prefix': vehicle.prefix,
      'group': vehicle.group,
      'name': vehicle.name,
      'accessibility': accessibility
    }
  }

}