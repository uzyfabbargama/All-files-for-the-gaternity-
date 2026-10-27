import { Router } from "express";
import { agregarItem, catalogo, comprar } from "../controllers/shopController.js";
import { requerirRol, verificarToken } from "../middleware/authMiddleware.js";

export const shopRoutes = Router();

shopRoutes.get("/catalog", catalogo);

shopRoutes.use(verificarToken);
shopRoutes.post("/purchase", comprar);

// Ruta protegida + autorizada por rol (RBAC)
shopRoutes.post("/items", requerirRol(["ADMIN", "EDITOR"]), agregarItem);
