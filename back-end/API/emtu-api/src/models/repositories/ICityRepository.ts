import { CityDto } from "../../dtos/cityDto";

interface ICityRepository {
  getAll() : Promise<CityDto[]>;
  getById(cityId: number) : Promise<CityDto>;
}

export { ICityRepository };