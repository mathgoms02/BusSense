
export default class BusRoute {
  routeShortName: string;
  routeNameStart: string;
  routeNameEnd: string;
  routeType: number;

  constructor(routeShortName: string, routeNameStart: string, routeNameEnd: string, routeType: number){
    this.routeShortName = routeShortName;
    this.routeNameStart = routeNameStart;
    this.routeNameEnd = routeNameEnd;
    this.routeType = routeType;
  }
};
