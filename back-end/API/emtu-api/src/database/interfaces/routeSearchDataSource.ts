import { RouteSearchDto } from "../../dtos/routeSearchDto";
// import RouteSearch from "../../models/routeSearch";

export default interface IRouteSearchDataSource {
  create(params: RouteSearchDto): Promise<any>;
}
