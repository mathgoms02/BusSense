import { CityDto } from "../../../../dtos/cityDto";

export interface IGetAllCities {
  execute(): Promise<CityDto[]>;
}