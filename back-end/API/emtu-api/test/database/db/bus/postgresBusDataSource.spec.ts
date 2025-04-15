import { QueryResult } from "pg";
import PostgresBusDataSource from "../../../../src/database/db/bus/postgresBusDataSource";

describe("PostgresBusDataSource", () => {
  describe("mapResultToModel", () => {
    it("should map the query result to a BusRoute array", () => {
      const queryResult = {
        rows: [
          {
            route_short_name: "038VP1",
            route_name_start: "SAO PAULO (SAO MIGUEL PAULISTA)",
            route_name_end: "SAO PAULO (METRO ARMENIA)",
            route_type: 3,
          },
          {
            route_short_name: "10",
            route_name_start: "Origin",
            route_name_end: "Destination",
            route_type: 2,
          },
        ],
      } as QueryResult;

      const expected = [
        {
          routeShortName: "038VP1",
          routeNameStart: "SAO PAULO (SAO MIGUEL PAULISTA)",
          routeNameEnd: "SAO PAULO (METRO ARMENIA)",
          routeType: 3,
        },
        {
          routeShortName: "10",
          routeNameStart: "Origin",
          routeNameEnd: "Destination",
          routeType: 2,
        },
      ];

      const result = PostgresBusDataSource.mapResultToModel(queryResult);
      expect(result).toEqual(expected);
    });
  });

  describe("PostgresBusDataSource", () => {
    describe("getRoute", () => {
      let postgresBusDataSource: PostgresBusDataSource;
      beforeAll(() => {
        postgresBusDataSource = new PostgresBusDataSource();
      });
  
      it("should return a BusRoute array for valid origin and destination", async () => {
        const result = await postgresBusDataSource.getRoute("Sao Paulo", "Guarulhos");
        expect(result).toBeDefined();
        expect(result.length).toBeGreaterThan(0);
        expect(result[0]).toHaveProperty("routeShortName");
        expect(result[0]).toHaveProperty("routeNameStart");
        expect(result[0]).toHaveProperty("routeNameEnd");
        expect(result[0]).toHaveProperty("routeType");
      });
  
      it("should return null for invalid origin and destination", async () => {
        await expect(await postgresBusDataSource.getRoute("InvalidOrigin", "InvalidDestination")).toBe(null);
      });
    });
  });
  
});
