
import BusRepository from './../../../src/models/repositories/implementations/BusRepository';
import PostgresBusDataSource from './../../../src/database/db/bus/postgresBusDataSource';
import AxiosBusExternal from '../../../src/external/axios/axiosBusExternal';
const busDataSource = new PostgresBusDataSource();
const busExternal = new AxiosBusExternal();
const busRepository = new BusRepository(busDataSource, busExternal);

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

describe('BusRepository', () => {
  describe('getRoute', () => {
    test('should return null for invalid origin or destination', async () => {
      expect(await busRepository.getRoute('', '')).toBe(null);
    });

    test('should return an array of routes for valid origin and destination', async () => {

    const controllerResult = await busRepository.getRoute('Sao paulo', 'Guarulhos');
    expect(controllerResult).toEqual(expected);
    });
  });
});