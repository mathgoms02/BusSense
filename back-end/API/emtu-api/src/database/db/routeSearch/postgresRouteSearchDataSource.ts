import { Pool } from "pg";
import { RouteSearchDto, FindRouteSearchDto, RankingSearchDto, RankingResultDto } from "../../../dtos/routeSearchDto";
import { InvalidParamError } from "../../../errors/invalidParamError";
import IRouteSearchDataSource from "../../interfaces/routeSearchDataSource";
import PostgresDB from "../postgresDB";

export class PostgresRouteSearchDataSource implements IRouteSearchDataSource {
  private dataBase: Pool;

  constructor() {
    this.dataBase = PostgresDB.getInstance();
  }

  public static async validate(params: RouteSearchDto) {
    const missingParams = ['idCidadeOrigem', 'idCidadeDestino'].filter(
      requiredParam => !params[requiredParam]
    );

    if (missingParams.length === 0) return;

    throw new InvalidParamError(`Parâmetros obrigatórios não informados: ${missingParams}`);
  }

  async create(params: RouteSearchDto): Promise<any> {
    await PostgresRouteSearchDataSource.validate(params);

    const query = {
      text: `INSERT INTO searches(id_cidade_origem, id_cidade_destino, id_cid, id_linha, sucedida, data_viagem, hora_viagem, data_criacao)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING *`,
      values: [
        params.idCidadeOrigem,
        params.idCidadeDestino,
        params.idCid,
        params.idLinha,
        params.sucedida,
        params.dataViagem,
        params.horaViagem,
        params.dataCriacao
      ],
    };

    const { rows } = await this.dataBase.query(query);

    return rows[0];
  };

  async get(params: FindRouteSearchDto): Promise<RouteSearchDto[]> {
    const queryFilters: string[] = [];
  
    if (this.isParamFilled(params.origin)) {
      queryFilters.push(`id_cidade_origem = ${params.origin}`);
    }

    if (this.isParamFilled(params.destination)) {
      queryFilters.push(`id_cidade_destino = ${params.destination}`);
    }

    if (this.isParamFilled(params.line)) {
      queryFilters.push(`id_linha = '${params.line}'`);
    }

    if (this.isParamFilled(params.startDate)) {
      queryFilters.push(`data_criacao::Date >= '${params.startDate}'::Date`);
    }

    if (this.isParamFilled(params.endDate)) {
      queryFilters.push(`data_criacao::Date <= '${params.endDate}'::Date`);
    }
  
    const whereClause = queryFilters.join(' AND ');

    const query = `SELECT * FROM searches WHERE ${whereClause}`;

    const { rows } = await this.dataBase.query(query);

    return PostgresRouteSearchDataSource.mapResultToModel(rows);
  };

  async getRanking(params: RankingSearchDto): Promise<RankingResultDto[]> {
    const queryFilters: string[] = [];
  
    if (this.isParamFilled(params.sucedida)) {
      queryFilters.push(`sucedida = '${params.sucedida}'`);
    }

    if (this.isParamFilled(params.idCid)) {
      queryFilters.push(`id_cid = ${params.idCid}`);
    }

    if (this.isParamFilled(params.startDate)) {
      queryFilters.push(`data_criacao::Date >= '${params.startDate}'::Date`);
    }

    if (this.isParamFilled(params.endDate)) {
      queryFilters.push(`data_criacao::Date <= '${params.endDate}'::Date`);
    }
  
    const whereClause = queryFilters.join(' AND ');
    const limitFilter = this.isParamFilled(params.limite) ? 
                        `LIMIT ${params.limite}` : "";

    const query = `SELECT id_linha, count(*) as qtd_buscas
                  FROM searches 
                  WHERE ${whereClause} 
                  GROUP BY id_linha 
                  ORDER BY count(*) desc
                  ${limitFilter}`;

    const { rows } = await this.dataBase.query(query);

    return rows.map((row) => ({
      idLinha: row.id_linha,
      searchCount: row.qtd_buscas
    }));
  };

  isParamFilled(param: any) {
    return param !== null && param !== undefined && param !== ''
  } 

  private static mapResultToModel(rows): RouteSearchDto[] {
    return rows.map((row) => ({
      id: row.id,
      idCidadeOrigem: row.id_cidade_origem,
      idCidadeDestino: row.id_cidade_destino,
      idLinha: row.id_linha,
      sucedida: row.sucedida,
      idCid: row.id_cid,
      dataViagem: row.data_viagem,
      horaViagem: row.hora_viagem,
      dataCriacao: row.data_criacao,
    }))
  }
}
