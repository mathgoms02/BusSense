import City from "../../city";
import { ICityRepository } from "../../repositories/ICityRepository";
import { IGetCityById } from "./interfaces/IGetCityById";

export class GetCityByIdUseCase implements IGetCityById {
  cityRepository: ICityRepository;
  constructor(cityRepository: ICityRepository){
    this.cityRepository = cityRepository;
  };

  async execute(cityId: number): Promise<City> {
    const city = await this.cityRepository.getById(cityId);
    if(city && city.id && city.name) {
      return new City(city.id, city.name);
    }
    return null
  };
}