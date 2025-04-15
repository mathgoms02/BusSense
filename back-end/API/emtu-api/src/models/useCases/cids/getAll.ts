import { CidsDto } from "../../../dtos/cidsDto";
import { ICidsRepository } from "../../repositories/ICidsRepository";
import { IGetAllCids } from "./interfaces/IGetAllCids";

export class GetAllCidsUseCase implements IGetAllCids{
  cidsRepository: ICidsRepository;

  constructor(cityRepository: ICidsRepository){
    this.cidsRepository = cityRepository
  }

  async execute(): Promise<CidsDto[]> {
      const cids = await this.cidsRepository.getAll();
      return cids;
  }
}