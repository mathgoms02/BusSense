export type RouteSearchDto = {
  idCidadeOrigem: number,
  idCidadeDestino: number,
  idLinha?: string,
  sucedida: boolean,
  idCid: number,
  dataViagem: string,
  horaViagem: string,
  dataCriacao: string
};

export type FindRouteSearchDto = {
  origin?: number,
  destination?: number,
  startDate?: string,
  endDate?: string,
  line?: string
};

export type RankingSearchDto = {
  sucedida?: boolean,
  startDate?: string,
  endDate?: string,
  idCid?: number,
  limite?: number
};

export type RankingResultDto = {
  idLinha: string,
  searchCount: number
};
