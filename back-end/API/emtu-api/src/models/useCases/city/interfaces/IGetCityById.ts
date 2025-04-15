import City from "../../../city";

export interface IGetCityById {
  execute(cityId: number) : Promise<City>;
};