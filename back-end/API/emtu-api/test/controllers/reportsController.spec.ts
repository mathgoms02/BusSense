import request from 'supertest';
import express from "express";
import bodyParser from "body-parser";
import ReportsController from '../../src/controllers/reportsController';
import { PostgresReportsDataSource } from '../../src/database/db/reports/postgresReportsDataSource';
import { InvalidParamError } from '../../src/errors/invalidParamError';

const reportsRoutes = express();

reportsRoutes.use(bodyParser.json());
reportsRoutes.post('/', ReportsController.create);

jest.mock('../../src/database/db/reports/postgresReportsDataSource');

describe('ReportsController', () => {
  describe('create', () => {
    afterEach(() => {
      jest.clearAllMocks();
    });

    it('should return 400 when throws a InvalidParamError', async () => {
      const createMock = jest.spyOn(PostgresReportsDataSource.prototype, 'create');

      createMock.mockRejectedValueOnce(new InvalidParamError('Message'));

      const response = await request(reportsRoutes)
        .post('/')
        .send({ email: 'test@mail.com', idCidadeOrigem: 1, idCidadeDestino: 2, idCid: 3 })
        .set('Content-type', 'application/json')

      expect(createMock).toHaveBeenCalledTimes(1);
      expect(response.status).toBe(400);
    });

    it('should return 500 when throws a another error', async () => {
      const createMock = jest.spyOn(PostgresReportsDataSource.prototype, 'create');

      createMock.mockRejectedValueOnce(new Error('Message'));

      const response = await request(reportsRoutes)
        .post('/')
        .send({ email: 'test@mail.com', idCidadeOrigem: 1, idCidadeDestino: 2, idCid: 3 })
        .set('Content-type', 'application/json')

      expect(createMock).toHaveBeenCalledTimes(1);
      expect(response.status).toBe(500);
    });

    it('should return 201 when report is created', async () => {
      const report = { id: 1, email: 'test@email.com', idCidadeOrigem: 1, idCidadeDestino: 2, idCid: 3 };
      const createMock = jest.spyOn(PostgresReportsDataSource.prototype, 'create');

      createMock.mockResolvedValueOnce(report);

      const response = await request(reportsRoutes)
        .post('/')
        .send({ email: report.email, idCidadeOrigem: report.idCidadeOrigem, idCidadeDestino: report.idCidadeDestino, idCid: report.idCid })
        .set('Content-type', 'application/json')

      expect(response.status).toBe(201);
      expect(createMock).toHaveBeenCalledTimes(1);
      expect(response.body).toEqual({ message: 'Solicitação criada com sucesso', report });
    });
  });
});
