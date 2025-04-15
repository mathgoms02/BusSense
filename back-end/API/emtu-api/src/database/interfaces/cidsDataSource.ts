import { CidsDto } from "../../dtos/cidsDto";

export default interface ICidsDataSource {
  getAll(): Promise<CidsDto[]>;
  getById(id: number): Promise<CidsDto>;
}