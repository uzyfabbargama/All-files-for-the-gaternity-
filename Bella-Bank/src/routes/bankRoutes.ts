// src/routes/bankRoutes.ts
import { Router } from "express";
import {
  cobrarCheque,
  depositar,
  emitirCheque,
  invertir,
  misFacturas,
  verFactura,
  verSaldo,
  verificarInversion,
} from "../controllers/bankController.js";
import { esPropietario, verificarToken } from "../middleware/authMiddleware.js";
import { getBillOwnerId } from "../services/bankService.js";
import { depositSchema, investSchema, transferSchema, validateBody } from "../middleware/validate.js";

export const bankRoutes = Router();

// Todas las rutas de banco requieren token JWT válido
bankRoutes.use(verificarToken);

bankRoutes.get("/balance", verSaldo);
bankRoutes.post("/deposit", validateBody(depositSchema), depositar);
bankRoutes.post("/invest", validateBody(investSchema), invertir);
bankRoutes.get("/invest/check", verificarInversion);

// 🔒 IDOR-safe por diseño: no acepta userId del cliente
bankRoutes.get("/bills/mine", misFacturas);

// 🔒 IDOR-safe por middleware de PROPIEDAD
// IMPORTANTE: esta ruta debe ir DESPUÉS de /bills/mine
bankRoutes.get(
  "/bills/:id",
  esPropietario((req) => getBillOwnerId(Number(req.params.id))),
  verFactura
);

bankRoutes.post("/bills", validateBody(transferSchema), emitirCheque);
bankRoutes.post("/bills/redeem", cobrarCheque);
