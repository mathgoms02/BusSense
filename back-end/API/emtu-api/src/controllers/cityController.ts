import { PostgresCityDataSource } from "../database/db/city/postgresCityDataSource";
import CityRepository from "../models/repositories/implementations/CityRepository";
import { GetAllCitiesUseCase } from "../models/useCases/city/getAllCities";
import { Request, Response } from "express";
import { GetCityByIdUseCase } from "../models/useCases/city/getCityById";

const cityDataSource = new PostgresCityDataSource();
const cityRepository = new CityRepository(cityDataSource);
const getAllCitiesUseCase = new GetAllCitiesUseCase(cityRepository);
const getCityByIdUseCase = new GetCityByIdUseCase(cityRepository);

export default class cityController {

  public static async getAllCities(req: Request, res: Response){
    try {
      const cities = await getAllCitiesUseCase.execute();
      return res.status(200).send(cities);
    } catch (error) {
      return res.status(500).send({ erro: "Erro ao obter dados" });
    }
  };

  public static async getCityById(req: Request, res: Response){
    const idCity = req.params.idCity;
    if(!idCity || parseInt(idCity) <= 0)
      return res.status(400).send({erro: "ID inválido"});
    try {
      const city = await getCityByIdUseCase.execute(parseInt(idCity));
      if(city == null) return res.status(400).send({erro: "Não foi possível encontrar a cidade"});
      return res.status(200).send({city: city});
    } catch (error) {
      return res.status(500).send({ erro: "Erro ao obter cidade" });
    }
  }

}

