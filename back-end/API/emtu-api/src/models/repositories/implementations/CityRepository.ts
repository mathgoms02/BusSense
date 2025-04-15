import ICityDataSource from "../../../database/interfaces/cityDataSource";
import cityDataSource from "../../../database/interfaces/cityDataSource";
import { CityDto } from "../../../dtos/cityDto";
import { ICityRepository } from "../ICityRepository";

export default class CityRepository implements ICityRepository {
  cityDataSource: ICityDataSource;

  constructor(cityDataSource: ICityDataSource) {
    this.cityDataSource = cityDataSource;
  }

  async getAll() : Promise<CityDto[]> {
    const cities = await this.cityDataSource.getAll();
    return cities;
  }

  async getById(cityId: number) : Promise<CityDto> {
    const city = await this.cityDataSource.getById(cityId);
    return city;
  }
}