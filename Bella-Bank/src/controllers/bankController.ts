// src/controllers/bankController.ts
import type { Response } from "express";
import type { AuthRequest } from "../middleware/authMiddleware.js";
import {
  checkInvestment,
  createBill,
  deposit,
  getBalance,
  getBillById,
  invest,
  listMyBills,
  redeemBill,
} from "../services/bankService.js";

export function verSaldo(req: AuthRequest, res: Response) {
  return res.json({ balanceCents: getBalance(req.user!.id) });
}

export function depositar(req: AuthRequest, res: Response) {
  try {
    const balance = deposit(req.user!.id, req.body.amountCents);
    return res.json({ mensaje: "Depósito exitoso", balanceCents: balance });
  } catch (e) {
    return res.status(400).json({ error: (e as Error).message });
  }
}

export function invertir(req: AuthRequest, res: Response) {
  try {
    return res.status(201).json(invest(req.user!.id, req.body.amountCents));
  } catch (e) {
    return res.status(400).json({ error: (e as Error).message });
  }
}

export function verificarInversion(req: AuthRequest, res: Response) {
  return res.json(checkInvestment(req.user!.id));
}

export function emitirCheque(req: AuthRequest, res: Response) {
  try {
    const bill = createBill(req.user!.id, req.body.amountCents);
    return res.status(201).json({
      codigo: bill.code,
      amountCents: bill.amount_cents,
      expiraEn: bill.expires_at,
    });
  } catch (e) {
    return res.status(400).json({ error: (e as Error).message });
  }
}

export function cobrarCheque(req: AuthRequest, res: Response) {
  try {
    const { code } = req.body as { code: string };
    const amount = redeemBill(req.user!.id, code);
    return res.json({
      mensaje: "Cheque cobrado",
      amountCents: amount,
      balanceCents: getBalance(req.user!.id),
    });
  } catch (e) {
    return res.status(400).json({ error: (e as Error).message });
  }
}

// 🔒 IDOR-safe por diseño: usa req.user.id, no un parámetro del cliente
export function misFacturas(req: AuthRequest, res: Response) {
  return res.json({ facturas: listMyBills(req.user!.id) });
}

// 🔒 El middleware esPropietario ya validó; aquí solo servimos
export function verFactura(req: AuthRequest, res: Response) {
  const billId = Number(req.params.id);
  const bill = getBillById(req.user!.id, billId);
  if (!bill) return res.status(404).json({ error: "Factura no encontrada" });
  return res.json(bill);
}
