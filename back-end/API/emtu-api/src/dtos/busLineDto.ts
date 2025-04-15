
export type BusLineDto = {
  code: string,
  origin: string,
  destination: string,
  lineHours: Date[],
  busStops: string[],
  prefix: string[],
  vehicle: Object,
}