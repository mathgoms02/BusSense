import PostgresBusDataSource from "../../../src/database/db/bus/postgresBusDataSource";
import { PostgresCityDataSource } from "../../../src/database/db/city/postgresCityDataSource";
import AxiosBusExternal from "../../../src/external/axios/axiosBusExternal";
import BusRepository from "../../../src/models/repositories/implementations/BusRepository";
import CityRepository from "../../../src/models/repositories/implementations/CityRepository";
import { GetBusRoutesUseCase } from "../../../src/models/useCases/bus/getBusRoutes";
import { GetCityByIdUseCase } from "../../../src/models/useCases/city/getCityById";


const cityDataSource = new PostgresCityDataSource();
const cityRepository = new CityRepository(cityDataSource);
const getCityByIdUseCase = new GetCityByIdUseCase(cityRepository);
const getBusRoutesService = new PostgresBusDataSource();
const busExternal = new AxiosBusExternal();
const getBusRoutesRepository = new BusRepository(getBusRoutesService, busExternal);
const getBusRoutesUseCase = new GetBusRoutesUseCase(getBusRoutesRepository);

const expected = [
  {
    routeShortName: '139',
    routeNameStart: 'SAO PAULO (SAO MIGUEL PAULISTA)',
    routeNameEnd: 'GUARULHOS (TERMINAL METROPOLITANO CECAP)',
    routeType: 3,
  },
  {
    routeShortName: '825',
    routeNameStart: 'SAO PAULO (SAO MIGUEL PAULISTA)',
    routeNameEnd: 'GUARULHOS (CENTRO)',
    routeType: 3,
  },
];
describe('getBusRoutesUseCase', () => {
  test('should return null if origin or destination is null or empty', async () => {
    const result = await getBusRoutesUseCase.execute('São Paulo', '');
    expect(result).toBeNull();
    const resultNull = await getBusRoutesUseCase.execute(null, 'Guarulhos');
    expect(resultNull).toBeNull();
  })

  test('should return null if origin or destination is valid', async () => {
    const result = await getBusRoutesUseCase.execute('Ção Paulo', 'Guarulhos');
    expect(result).toBeNull()
  })

  test('should return result if origin and destination is valid', async () => {
    const result = await getBusRoutesUseCase.execute('São Paulo', 'Guarulhos');
    expect(result).toEqual(expected);
  })

  test('should return result if origin and destination has special characters', async () => {
    const result = await getBusRoutesUseCase.execute('São Paúlo', 'Guarûlhos');
    expect(result).toEqual(expected);
  })
});

