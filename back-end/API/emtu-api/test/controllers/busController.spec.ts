import request from 'supertest';
import express from "express";
import busController from '../../src/controllers/busController';

const busRoutes = express();

busRoutes.post('/', busController.getRoutes);

describe("find bus route", () => {
  test("should return 400 when passing an invalid body", async () => {
    const res = await request(busRoutes)
    .post('/')
    .set('Content-type', 'application/json').send({});
    expect(res.status).toBe(400);
    expect(res.body).toEqual({
      erro: 'Objeto enviado é inválido',
    });
  });

  test("should return 400 when passing null", async () => {
    const res = await request(busRoutes)
    .post('/')
    .set('Content-type', 'application/json').send(null);
    expect(res.status).toBe(400);
    expect(res.body).toEqual({
      erro: 'Objeto enviado é inválido',
    });
  });

  test("should return 400 when passing undefined", async () => {
    const res = await request(busRoutes)
    .post('/')
    .set('Content-type', 'application/json').send(undefined);
    expect(res.status).toBe(400);
    expect(res.body).toEqual({
      erro: 'Objeto enviado é inválido',
    });
  });
});