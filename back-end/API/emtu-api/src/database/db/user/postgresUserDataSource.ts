import { Pool, QueryResult } from "pg";
import { UserDto } from "../../../dtos/userDto";
import User from "../../../models/user";
import IUserDataSource from "../../interfaces/userDataSource";
import PostgresDB from "../postgresDB";

export class PostgresUserDataSource implements IUserDataSource {
  private dataBase: Pool;

  constructor() {
    this.dataBase = PostgresDB.getInstance();
  }

  async getByEmail(email: string): Promise<User> {
    const result = await this.dataBase.query(`SELECT * FROM users u WHERE u.email = $1;`, [email]);
    return result && result.rowCount > 0 ? PostgresUserDataSource.mapResultToModel(result)[0] : null;
  }

  async create(user: User): Promise<QueryResult<User>> {
    const data = await this.dataBase.query(
      `INSERT INTO users(name, email, password) VALUES ($1, $2, $3) RETURNING *`,
      [user.name, user.email, user.password]
    );
    return data && data.rowCount > 0 ? data.rows[0] : null;
  };

  private static mapResultToModel = (result: QueryResult<UserDto>): User[] => {
    return result ? result.rows.map(
      (row) => (new User(row.name, row.email, row.password))
    ) : null;
  }
} 