import { Pool } from "pg";
import { ReportDto } from "../../../dtos/reportDto";
import { InvalidParamError } from "../../../errors/invalidParamError";
import Report from "../../../models/report";
import IReportsDataSource from "../../interfaces/reportsDataSource";
import PostgresDB from "../postgresDB";
import { ReportsRequestDto, ReportsResponseDto} from "../../../dtos/reportDto";

export class PostgresReportsDataSource implements IReportsDataSource {
  private dataBase: Pool;

  constructor() {
    this.dataBase = PostgresDB.getInstance();
  }

  async create(params: ReportDto): Promise<Report> {
    await Report.validate(params);

    const reportExists = await this.exists(params);

    if (reportExists) {
      throw new InvalidParamError('Solicitação para esta rota já foi enviada');
    }

    const dataCriacao = new Date();
    const query = {
      text: `INSERT INTO reports(email, id_cidade_origem, id_cidade_destino, id_cid, data_criacao)
        VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      values: [
        params.email,
        params.idCidadeOrigem,
        params.idCidadeDestino,
        params.idCid,
        dataCriacao
      ],
    };

    const { rows } = await this.dataBase.query(query);

    return rows[0];
  };

  private async exists(params: ReportDto): Promise<boolean> {
    const query = {
      text: `SELECT * FROM reports
        WHERE email = $1
        AND id_cidade_origem = $2
        AND id_cidade_destino = $3
        AND id_cid = $4`,
      values: [
        params.email,
        params.idCidadeOrigem,
        params.idCidadeDestino,
        params.idCid,
      ],
    };

    const { rowCount } = await this.dataBase.query(query);

    return rowCount > 0;
  };

  async getReports(params: ReportsRequestDto): Promise<ReportsResponseDto[]> {
    const queryFilters: string[] = [];

    if (this.isParamFilled(params.email)) {
      queryFilters.push(`email = '${params.email}'`);
    }

    if (this.isParamFilled(params.idCid)) {
      queryFilters.push(`id_cid = ${params.idCid}`);
    }

    if (this.isParamFilled(params.destination)) {
      queryFilters.push(`id_cidade_destino = ${params.destination}`);
    }

    if (this.isParamFilled(params.origin)) {
      queryFilters.push(`id_cidade_origem = ${params.origin}`);
    }

    if (this.isParamFilled(params.startDate)) {
      queryFilters.push(`data_criacao::Date >= '${params.startDate}'::Date`);
    }

    if (this.isParamFilled(params.endDate)) {
      queryFilters.push(`data_criacao::Date <= '${params.endDate}'::Date`);
    }

    const whereClause = queryFilters.join(' AND ');
    const limitFilter = this.isParamFilled(params.limit) ?
                        `LIMIT ${params.limit}` : "";

    const query = `SELECT *
                  FROM reports
                  WHERE ${whereClause}
                  ${limitFilter}`;

    const { rows } = await this.dataBase.query(query);

    return rows
  };

  private isParamFilled(param: any) {
    return param !== null && param !== undefined && param !== ''
  }
}
