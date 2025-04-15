import { Request, Response } from "express";
import { PostgresRouteSearchDataSource } from "../database/db/routeSearch/postgresRouteSearchDataSource";
import { InvalidParamError } from "../errors/invalidParamError";
import { FindRouteSearchDto, RankingSearchDto } from "../dtos/routeSearchDto";

const routeSearchDataSource = new PostgresRouteSearchDataSource();

export default class RouteSearchesController {
  public static async get(req: Request, res: Response): Promise<Response> {
    try {
      const routeSearch = req.query as FindRouteSearchDto;
      RouteSearchesController.validateSearchParams(routeSearch);

      const data = await routeSearchDataSource.get(routeSearch);

      res.status(200).send({ data });
    } catch (error) {
      console.log(error)
      if (error instanceof InvalidParamError) {
        return res.status(400).send({ message: error.message });
      }

      return res.status(500).send({ message: 'Um erro inesperado aconteceu ao encontrar as buscas realizadas' });
    }
  }

  public static async getRanking(req: Request, res: Response): Promise<Response> {
    try {
      const rankingSearch = req.query as RankingSearchDto;
      RouteSearchesController.validateSearchParams(rankingSearch as FindRouteSearchDto);

      const data = await routeSearchDataSource.getRanking(rankingSearch);

      res.status(200).send({ data });
    } catch (error) {
      console.log(error)
      if (error instanceof InvalidParamError) {
        return res.status(400).send({ message: error.message });
      }

      return res.status(500).send({ message: 'Um erro inesperado aconteceu ao obter o ranking das linhas' });
    }
  }

  public static validateSearchParams(params: FindRouteSearchDto) {
    const missingParams = ['startDate', 'endDate'].filter(
      requiredParam => !params[requiredParam]
    );
    
    if (missingParams.length <= 1) return;

    throw new InvalidParamError(`Informe pelo menos um período: ${missingParams}`);
  }
}
