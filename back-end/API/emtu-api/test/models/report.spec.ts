import Report from "../../src/models/report";

describe('Report class', () => {
  test('should create an instance of Report with the correct properties', () => {
    const email = 'ayrton@senna.com';
    const idCidadeOrigem = 1;
    const idCidadeDestino = 2;
    const idCid = 3;

    const report = new Report(email, idCidadeOrigem, idCidadeDestino, idCid);

    expect(report.email).toBe(email);
    expect(report.idCidadeOrigem).toBe(idCidadeOrigem);
    expect(report.idCidadeDestino).toBe(idCidadeDestino);
    expect(report.idCid).toBe(idCid);
  });
});
