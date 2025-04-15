import BusRoute from "../../busRoute";
import { IBusRepository } from "../../repositories/IBusRepository";
import { IGetLine } from "./interfaces/IGetLine";
import BusLine from "../../busLine";
import moment from "moment";
import { BusLineDto } from "../../../dtos/busLineDto";

export default class GetLineUsecase implements IGetLine {
  constructor(getBusRoutesRepository: IBusRepository) {
    this.getBusRoutesRepository = getBusRoutesRepository;
  }
  getBusRoutesRepository: IBusRepository;
  async execute(busRoute: BusRoute[], date: Date, hour: Date, originCity: string, destinyCity : string): Promise<BusLineDto[]> {
    try {
      let routes = await this.getBusRoutesRepository.getLines(busRoute);
      let lineDetails: BusLine[];
      let lines: BusLineDto[] = [];
      if (routes == null) return lines;

      lineDetails = BusLine.fromJson(routes, originCity, destinyCity);

      const dayOfWeek = date.getDay();
      // console.log(`Data: ${date}, dia da semana: ${date.getDay()}`);
      // console.log(`Hora solicitada: ${hour}`);
      // console.log(`Total de rotas antes do filtro: ${lineDetails.length}`);
      lineDetails.forEach((line) => {
        let hours = this.getHours(dayOfWeek, line, hour);
        // console.log(`Linha ${line.codigo}: horários disponíveis = ${hours.length}`);
        if(hours.length > 0){
          lines.push({
            code: line.codigo,
            origin: line.cidade_origem,
            destination: line.cidade_destino,
            lineHours: hours,
            busStops: line.pontos,
            prefix: line.prefixo,
            vehicle: null,
          })
        }
        // console.log(`Total de rotas após filtro: ${lines.length}`);
      });

      return lines;
    } catch (error) {
      throw(error);
    }
  }

  getHours(dayOfWeek: number, line: BusLine, requestHour): Date[] {
    if (dayOfWeek >= 1 && dayOfWeek <= 5 && line.horariosdiasuteis.length > 0) // dias uteis (segunda a sexta)
      return line.horariosdiasuteis.filter(hour => hour >= requestHour)
    if (dayOfWeek == 6 && line.horariossabados.length > 0) // sábado
      return line.horariossabados.filter(hour => hour >= requestHour)
    if (dayOfWeek == 0 && line.horariosdomingosferiados.length > 0) // domingo
      return line.horariosdomingosferiados.filter(hour => hour >= requestHour)
    return line.horarios.filter(hour => hour >= requestHour);
  }
}

