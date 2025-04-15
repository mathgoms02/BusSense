import request from 'supertest';
import express from "express";
import bodyParser from "body-parser";
import RouteSearchesController from '../../src/controllers/routeSearchesController';
import { PostgresRouteSearchDataSource } from '../../src/database/db/routeSearch/postgresRouteSearchDataSource';

const routeSearchRoutes = express();

routeSearchRoutes.use(bodyParser.json());
routeSearchRoutes.get('/', RouteSearchesController.get);

jest.mock('../../src/database/db/routeSearch/postgresRouteSearchDataSource');

describe('RouteSearchesController', () => {
  describe('get', () => {
    afterEach(() => {
      jest.clearAllMocks();
    });

    it('should return 200 when search is sucessful', async () => {
      const routeSearch = { 
        startDate: '2023/08/26', 
      };

      const result = [{
        idCidadeOrigem: 1,
        idCidadeDestino: 2,
        idLinha: '086',
        sucedida: true,
        idCid: 1,
        dataViagem: '2023/09/26',
        horaViagem: '18:00',
        dataCriacao: '2023/08/26'
      }]

      const createMock = jest.spyOn(PostgresRouteSearchDataSource.prototype, 'get');
      createMock.mockResolvedValue(result)

      const response = await request(routeSearchRoutes)
        .get('/')
        .query(routeSearch)
        .set('Content-type', 'application/json')

      expect(response.status).toBe(200);
      expect(createMock).toHaveBeenCalledTimes(1);
      expect(response.body).toEqual({ data: result });
    });

    it('should return 400 when param is invalid', async () => {
      const routeSearch = [{ 
        startDate: '', 
      }];
      const createMock = jest.spyOn(PostgresRouteSearchDataSource.prototype, 'get');

      const response = await request(routeSearchRoutes)
        .get('/')
        .query(routeSearch)
        .set('Content-type', 'application/json')

      expect(response.status).toBe(400);
      expect(createMock).toHaveBeenCalledTimes(0);
      expect(response.body).toEqual({ message: 'Informe pelo menos um período: startDate,endDate' });
    });
  });
});
