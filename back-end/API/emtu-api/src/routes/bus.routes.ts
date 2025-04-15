import { Router } from "express";
import busController from "../controllers/busController";

const busRoutes = Router();

busRoutes.post("/", busController.getRoutes);

export { busRoutes };