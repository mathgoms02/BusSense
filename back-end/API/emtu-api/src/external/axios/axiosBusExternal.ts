
import axios from 'axios';
import { IBusExternal } from '../interfaces/busExternal';
import BusRoute from './../../models/busRoute';
import dotenv from "dotenv";

dotenv.config();

export default class AxiosBusExternal implements IBusExternal {
  async getLinesDetails(busRoutes : BusRoute[]) {
    return await Promise.all(busRoutes.map((route)=> this.getFromEmtuApi(route.routeShortName)));
  }

  getFromEmtuApi(lineId: string){
    return axios.get(`${process.env.EMTU_API}/lineDetails?linha=${lineId}`);
  }
};