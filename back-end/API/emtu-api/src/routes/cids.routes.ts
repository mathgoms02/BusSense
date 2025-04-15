import { Router } from "express";
import cidsController from "../controllers/cidsController";

const cidsRoutes = Router();

cidsRoutes.get('/', cidsController.getAll)

export {cidsRoutes};