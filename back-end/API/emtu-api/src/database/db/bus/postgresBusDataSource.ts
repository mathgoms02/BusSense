import { Pool, QueryResult } from "pg";
import IBusDataSource from "../../interfaces/busDataSource";
import PostgresDB from "../postgresDB";
import BusRoute from "../../../models/busRoute";

export default class PostgresBusDataSource implements IBusDataSource {
  private dataBase: Pool;

  constructor(){
    this.dataBase = PostgresDB.getInstance();
  };

  async getRoute(origin: string, destination: string): Promise<BusRoute[]> {
    try {
      const result = await this.
      dataBase.query(
        `SELECT * FROM bus_routes WHERE 
        route_name_start ilike $1
        AND route_name_end ilike $2 `
      , [`${origin}%`, `${destination}%`]);

      return result.rowCount > 0 ? PostgresBusDataSource.mapResultToModel(result) : null;
    } catch (error) {
      throw(error);
    }
  };

  public static mapResultToModel = (result: QueryResult): BusRoute[] => {
    return result.rows.map((row) => ({
      routeShortName: row.route_short_name,
      routeNameStart: row.route_name_start,
      routeNameEnd: row.route_name_end,
      routeType: row.route_type,
    }));
  };
};
