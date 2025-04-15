import ICidsDataSource from "../../../database/interfaces/cidsDataSource";
import { CidsDto } from "../../../dtos/cidsDto";
import { ICidsRepository } from "../ICidsRepository";

export default class CidsRepository implements ICidsRepository {
  cidsDataSource: ICidsDataSource;

  constructor(cidsDataSource: ICidsDataSource) {
    this.cidsDataSource = cidsDataSource;
  }
  
  async getById(id: number): Promise<CidsDto> {
    return await this.cidsDataSource.getById(id);
  }

  async getAll() : Promise<CidsDto[]> {
    return await this.cidsDataSource.getAll();
  }
}