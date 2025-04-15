import { Pool } from "pg";
import { PostgresReportsDataSource } from "../../../../src/database/db/reports/postgresReportsDataSource";
import { ReportDto } from "../../../../src/dtos/reportDto";
import { InvalidParamError } from "../../../../src/errors/invalidParamError";
import PostgresDB from "../../../../src/database/db/postgresDB";

describe('PostgresReportsDataSource', () => {
  let dataSource: PostgresReportsDataSource;
  let mockPool: jest.Mocked<Pool>;

  beforeEach(() => {
    mockPool = { query: jest.fn() } as any;
    jest.spyOn(PostgresDB, 'getInstance').mockReturnValue(mockPool);
    dataSource = new PostgresReportsDataSource();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('create', () => {
    const params: ReportDto = {
      email: 'test@test.com',
      idCidadeOrigem: 1,
      idCidadeDestino: 2,
      idCid: 3,
    };

    it('should validate params before creating report', async () => {
      const invalidReportDto = { ...params, email: 'invalidEmail' };

      await expect(dataSource.create(invalidReportDto)).rejects.toThrow(InvalidParamError);

      expect(mockPool.query).not.toHaveBeenCalled();
    });

    it('should throw InvalidParamError if report with same params already exists', async () => {
      mockPool.query.mockResolvedValueOnce({ rowCount: 1 } as never);

      await expect(dataSource.create(params)).rejects.toThrow(InvalidParamError);

      expect(mockPool.query).toHaveBeenCalledTimes(1);
      expect(mockPool.query).toHaveBeenCalledWith({
        text: expect.stringContaining('SELECT * FROM reports'),
        values: [params.email, params.idCidadeOrigem, params.idCidadeDestino, params.idCid],
      });
    });

    it('should insert new report if report with same params does not exist', async () => {
      mockPool.query.mockResolvedValueOnce({ rowCount: 0 } as never);

      const currentDate = new Date();
      jest.spyOn(global, 'Date').mockImplementation(() => currentDate as any);

      const expectedReport = { ...params, id: 1, dataCriacao: currentDate };
      mockPool.query.mockResolvedValueOnce({ rows: [expectedReport] } as never);

      const createdReport = await dataSource.create(params);

      expect(createdReport).toEqual(expectedReport);
      expect(mockPool.query).toHaveBeenCalledTimes(2);
      expect(mockPool.query).toHaveBeenNthCalledWith(1, {
        text: expect.stringContaining('SELECT * FROM reports'),
        values: [params.email, params.idCidadeOrigem, params.idCidadeDestino, params.idCid],
      });
      expect(mockPool.query).toHaveBeenNthCalledWith(2, {
        text: expect.stringContaining('INSERT INTO reports'),
        values: [
          params.email,
          params.idCidadeOrigem,
          params.idCidadeDestino,
          params.idCid,
          currentDate,
        ],
      });
    });
  });
});
