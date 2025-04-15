import {PostgresCidsDataSource} from "../database/db/cids/potsgresCidsDataSource";
import CidsRepository from "../models/repositories/implementations/CidsRepository";
import { GetAllCidsUseCase } from "../models/useCases/cids/getAll";
import { Request, Response} from "express";

const cidsDataSource = new PostgresCidsDataSource();
const cidsRepository = new CidsRepository(cidsDataSource);
const getAllCidsUseCase = new GetAllCidsUseCase(cidsRepository);

export default class cidsController {
  public static async getAll(req: Request, res: Response){
    try{
      const cids = await getAllCidsUseCase.execute()
      return res.status(200).send(cids)
    }catch(err){
      return res.status(500).send({mensagem: "Erro ao obter cids"});
    }
  }
}