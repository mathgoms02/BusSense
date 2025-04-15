import { Pool, QueryResult } from "pg";
import { VehicleDto } from "../../../dtos/vehicleDto";
import { IVehicleDatasource } from "../../interfaces/vehiclesDatasource";
import PostgresDB from "../postgresDB";
import { setPlaceholders } from "../../../utils/arrayUtils";

export class PostgresVehicleDatasource implements IVehicleDatasource {
  private dataBase: Pool;

  constructor(){
    this.dataBase = PostgresDB.getInstance();
  };

  async getByPrefix(prefix: string[]): Promise<VehicleDto[]> {
    if(!prefix.length) return null;
    const sql = `SELECT * FROM vehicles v WHERE v.prefix in ${setPlaceholders(prefix)};`; 
    const result = await this.dataBase.query(sql, prefix);
    return result && result.rowCount > 0 ? PostgresVehicleDatasource.mapResultToModel(result) : [];
  }

  private static mapResultToModel = (result: QueryResult<VehicleDto>): VehicleDto[] => {
    return result ? result.rows.map(
      (row) => ({
        id: row.id,
        prefix: row.prefix,
        name: row.name,
        group: row.group,
        accessibility: null,
      }))
     : null;
  }  
}