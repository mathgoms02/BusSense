import { CityDto } from "../../../src/dtos/cityDto";
import City from "../../../src/models/city";
import { ICityRepository } from "../../../src/models/repositories/ICityRepository";
import { GetCityByIdUseCase } from "../../../src/models/useCases/city/getCityById";
import {jest, test} from '@jest/globals';

describe("GetCityByIdUseCase", () => {
  let getCityByIdUseCase: GetCityByIdUseCase;

  const cityRepositoryMock = { 
    getById: jest.fn<() => Promise<CityDto>>(),
  } as unknown as ICityRepository;
  
  beforeEach(() => {
    getCityByIdUseCase = new GetCityByIdUseCase(cityRepositoryMock);
  });

  describe("execute", () => {
    test("should return null if city does not exist", async () => {
      (cityRepositoryMock.getById as jest.Mock).mockResolvedValueOnce(null);

      const cityId = 0;
      const result = await getCityByIdUseCase.execute(cityId);
      expect(result).toBeNull();
    });

    test("should return a City object if city exists", async () => {
      const cityData = { id: 1, name: "City" };
      (cityRepositoryMock.getById as jest.Mock).mockResolvedValueOnce(cityData);

      const cityId = 1;
      const result = await getCityByIdUseCase.execute(cityId);

      expect(result).toBeInstanceOf(City);
      expect(result.getId()).toBe(cityData.id);
      expect(result.getName()).toBe(cityData.name);
    });

    test("should return null if city is missing id or name property", async () => {
      const cityData = { name: "City Name", id: null };
      (cityRepositoryMock.getById as jest.Mock).mockResolvedValueOnce(cityData);

      const cityId = 1;
      const result = await getCityByIdUseCase.execute(cityId);

      expect(result).toBeNull();
    });
  });
});
