import { Pool } from "pg";
import { PostgresRouteSearchDataSource } from "../../../../src/database/db/routeSearch/postgresRouteSearchDataSource";
import { RouteSearchDto } from "../../../../src/dtos/routeSearchDto";
import { InvalidParamError } from "../../../../src/errors/invalidParamError";
import PostgresDB from "../../../../src/database/db/postgresDB";

describe('PostgresRouteSearchDataSource', () => {
  let dataSource: PostgresRouteSearchDataSource;
  let mockPool: jest.Mocked<Pool>;

  beforeEach(() => {
    mockPool = { query: jest.fn() } as any;
    jest.spyOn(PostgresDB, 'getInstance').mockReturnValue(mockPool);
    dataSource = new PostgresRouteSearchDataSource();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('create', () => {
    const params: RouteSearchDto = {
      idCidadeOrigem: 1,
      idCidadeDestino: 2,
      idCid: 3,
      dataViagem: '2023-10-05',
      horaViagem: '10:25',
      idLinha: "001",
      sucedida: false,
      dataCriacao: '2023-10-05'
    };

    it('should validate params before creating route search', async () => {
      const invalidRouteSearchDto = { ...params, idCidadeOrigem: null };

      await expect(dataSource.create(invalidRouteSearchDto)).rejects.toThrow(InvalidParamError);

      expect(mockPool.query).not.toHaveBeenCalled();
    });

    it('should insert new route search if params are valid', async () => {
      const expectedRouteSearch = { ...params, id: 1 };
      mockPool.query.mockResolvedValueOnce({ rows: [expectedRouteSearch] } as never);

      const createdRouteSearch = await dataSource.create(params);

      expect(createdRouteSearch).toEqual(expectedRouteSearch);
      expect(mockPool.query).toHaveBeenCalledWith({
        text: expect.stringContaining('INSERT INTO searches'),
        values: [
          params.idCidadeOrigem,
          params.idCidadeDestino,
          params.idCid,
          params.idLinha,
          params.sucedida,
          params.dataViagem,
          params.horaViagem,
          params.dataCriacao,
        ],
      });
    });
  });
});
