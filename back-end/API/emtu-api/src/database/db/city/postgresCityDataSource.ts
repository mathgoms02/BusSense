import { Pool, QueryResult } from "pg";
import { CityDto } from "../../../dtos/cityDto";
import cityDataSource from "../../interfaces/cityDataSource";
import PostgresDB from "../postgresDB";

export class PostgresCityDataSource implements cityDataSource {
  private dataBase: Pool;

  constructor(){
    this.dataBase = PostgresDB.getInstance();
  }

  async getAll(): Promise<CityDto[]> {
    const result = await this.dataBase.query(`SELECT * FROM city c;`);
    return PostgresCityDataSource.mapResultToModel(result);
  };

  async getById(cityId: number): Promise<CityDto> {
    const result = await this.dataBase.query(`SELECT * FROM city c WHERE c.id = $1 LIMIT 1`, [cityId]);
    return { id: result.rows[0]?.id, name: result.rows[0]?.name}
  };
  
  private static mapResultToModel = (result: QueryResult): CityDto[] => result.rows.map((row) => ({ id: row.id, name: row.name}))
} 