import { Pool } from "pg";
import dotenv from "dotenv";

dotenv.config();

class PostgresDB {
  private static _instance: Pool;
  private constructor() {}

  public static getInstance(): Pool {
    if(this._instance) {
      return this._instance;
    }

    this._instance = new Pool({
      connectionString: process.env.DATABASE_URL
    });

    this._instance.on('connect', () => {
      console.log('Base de Dados conectada com sucesso!');
    });

    return this._instance;
  }
}

export default PostgresDB;

