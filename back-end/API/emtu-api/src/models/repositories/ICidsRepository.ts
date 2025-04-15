import { CidsDto } from "../../dtos/cidsDto";

interface ICidsRepository {
  getAll() : Promise<CidsDto[]>
  getById(id: number) : Promise<CidsDto>
}

export {ICidsRepository}