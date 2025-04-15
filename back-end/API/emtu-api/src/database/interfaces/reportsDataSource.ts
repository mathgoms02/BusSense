import { ReportDto } from '../../dtos/reportDto';
import Report from '../../models/report';

export default interface IReportsDataSource {
  create(params: ReportDto): Promise<Report>;
}
