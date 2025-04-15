import { CityDto } from "../../../dtos/cityDto";
import { ICityRepository } from "../../repositories/ICityRepository";
import { IGetAllCities } from "./interfaces/IGetAllCities";

export class GetAllCitiesUseCase implements IGetAllCities{
  cityRepository: ICityRepository;
  constructor(cityRepository: ICityRepository){
    this.cityRepository = cityRepository;
  };

  async execute(): Promise<CityDto []> {
    const cities = await this.cityRepository.getAll();
    return cities;
  };

}