export type ReportDto = {
  dataCriacao?: Date,
  email: string,
  idCidadeOrigem: number,
  idCidadeDestino: number,
  idCid: number
};

export type ReportsRequestDto = {
  origin?: number,
  destination?: number,
  startDate?: boolean,
  idCid?: number,
  endDate?: string,
  email?: string,
  limit?: number
};

export type ReportsResponseDto = {
  email?: string,
  idCidadeOrigem?: number,
  idCidadeDestino?: number,
  idCid?: number,
  dataCriacao?: string,
  id?: number,
};


