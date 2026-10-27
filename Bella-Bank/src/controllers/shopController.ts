import type { Response } from "express";
import type { AuthRequest } from "../middleware/authMiddleware.js";
import { addOrRestock, getCatalog, purchaseItem } from "../services/shopService.js";

export function catalogo(_req: AuthRequest, res: Response) {
  return res.json(getCatalog());
}

export function comprar(req: AuthRequest, res: Response) {
  try {
    const { name } = req.body as { name: string };
    const bill = purchaseItem(req.user!.id, name);
    return res.status(201).json({
      mensaje: "Factura generada. Cóbresela en /bank/bills/redeem",
      factura: { codigo: bill.code, amountCents: bill.amount_cents },
    });
  } catch (e) {
    return res.status(400).json({ error: (e as Error).message });
  }
}

// Solo ADMIN puede reestockear
export function agregarItem(req: AuthRequest, res: Response) {
  const { name, stock, price } = req.body as { name: string; stock: number; price: number };
  addOrRestock(name, stock, price);
  return res.status(201).json({ mensaje: "Ítem agregado/actualizado" });
}
