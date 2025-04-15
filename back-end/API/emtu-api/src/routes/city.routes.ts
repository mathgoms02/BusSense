import { Router } from "express";
import cityController from './../controllers/cityController';

const cityRoutes = Router();

cityRoutes.get('/', cityController.getAllCities);
cityRoutes.get('/:idCity', cityController.getCityById);

export { cityRoutes }

