
export default class BusLine {
  codigo: string;
  cidade_origem: string;
  cidade_destino: string;
  horarios: Date[];
  pontos: string[];
  horariosdiasuteis: Date[];
  horariossabados: Date[];
  horariosdomingosferiados: Date[];
  prefixo: string[];

  constructor(codigo: string,cidade_origem: string,cidade_destino: string,
    horarios: Date[],
    pontos: string[],
    horariosdiasuteis: Date[],
    horariossabados: Date[],
    horariosdomingosferiados: Date[],
    prefixo: string[]
    ){
    this.codigo = codigo;
    this.cidade_origem = cidade_origem;
    this.cidade_destino = cidade_destino;
    this.horarios = horarios;
    this.pontos = pontos;
    this.horariosdiasuteis = horariosdiasuteis;
    this.horariossabados = horariossabados;
    this.horariosdomingosferiados = horariosdomingosferiados;
    this.prefixo = prefixo;
  }

  static fromJson(obj: any, originCity: string, destinyCity: string): BusLine[]{
    let lineDetails: BusLine[] = [];
    obj.filter(route=> route.data.linhas.length > 0).map(route => {
        let lines = route.data.linhas[0];
        let lineRoutes = lines.rotas
        lineRoutes.forEach(line =>{
          const normalize = (str: string): string =>
            str
                .normalize('NFD') // Decompõe caracteres acentuados
                .replace(/[\u0300-\u036f]/g, '') // Remove os acentos
                .toLowerCase(); // Converte para minúsculas
          if (normalize(line.cidade).includes(normalize(originCity)) || normalize(originCity).includes(normalize(line.cidade))) {
            let busLine = new BusLine(
              lines.codigo,
              line.cidade,
              line.destino,
              line.horarios.split(',').map(hour => new Date('1/1/1999 ' + hour)),
              line.pontos,
              line.horariosdiasuteis.split(',').map(hour => new Date('1/1/1999 ' + hour)),
              line.horariossabados.split(',').map(hour => new Date('1/1/1999 ' + hour)),
              line.horariosdomingosferiados.split(',').map(hour => new Date('1/1/1999 ' + hour)),
              lines.veiculos.map(veiculo => veiculo.prefixo)
              );
            lineDetails.push(busLine);
          }
        })
    });
    return lineDetails;
  }
}
