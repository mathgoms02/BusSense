import { Request, Response } from "express";
import { PostgresReportsDataSource } from "../database/db/reports/postgresReportsDataSource";
import { InvalidParamError } from "../errors/invalidParamError";
import { ReportsRequestDto, ReportsResponseDto } from "../dtos/reportDto"

const reportsDataSource = new PostgresReportsDataSource();

export default class ReportsController {
  public static async create(req: Request, res: Response): Promise<Response> {
    try {
      const { email, idCidadeOrigem, idCidadeDestino, idCid } = req.body;

      const report = await reportsDataSource.create({ email, idCidadeOrigem, idCidadeDestino, idCid });

      res.status(201).json({ message: 'Solicitação criada com sucesso', report });
    } catch (error) {
      if (error instanceof InvalidParamError) {
        return res.status(400).send({ message: error.message });
      }

      return res.status(500).send({ message: 'Um erro inesperado aconteceu no processamento da solicitação' });
    }
  }

  public static async getReports(req: Request, res: Response): Promise<Response> {
    try {
      const rankingSearch = req.query as ReportsRequestDto;
      ReportsController.validateGetReportsParams(rankingSearch as ReportsRequestDto);

      const data = await reportsDataSource.getReports(rankingSearch);

      res.status(200).send({ data });
    } catch (error) {
      console.log(error)
      if (error instanceof InvalidParamError) {
        return res.status(400).send({ message: error.message });
      }

      return res.status(500).send({ message: 'Um erro ao obter reports' });
    }
  }

  public static validateGetReportsParams(params: ReportsRequestDto) {
    const missingParams = ['startDate', 'endDate'].filter(
      requiredParam => !params[requiredParam]
    );

    if (missingParams.length <= 1) return;

    throw new InvalidParamError(`Informe pelo menos um período: ${missingParams}`);
  }
}
