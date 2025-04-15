import { Router } from "express";
import { busRoutes } from './bus.routes';
import { cidsRoutes } from "./cids.routes";
import { cityRoutes } from "./city.routes";
import { reportsRoutes } from "./reports.routes";
import { searchRoutes } from './search.routes';
import { userRoutes } from "./user.routes";

const router = Router();

router.use("/bus", busRoutes);
router.use("/cids", cidsRoutes);
router.use("/city", cityRoutes);
router.use("/reports", reportsRoutes);
router.use("/searches", searchRoutes);
router.use("/user", userRoutes);

export { router }
