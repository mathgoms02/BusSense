import { CidsDto } from "../../../../dtos/cidsDto";

export interface IGetAllCids {
  execute(): Promise<CidsDto[]>;
}