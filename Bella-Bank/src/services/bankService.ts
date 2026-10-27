import crypto from "node:crypto";
import { db } from "../db/database.js";
import type { Bill } from "../models/User.js";

export function getBalance(userId: number): number {
  const row = db.prepare("SELECT balance_cents FROM accounts WHERE user_id = ?").get(userId) as
    | { balance_cents: number }
    | undefined;
  return row?.balance_cents ?? 0;
}

export function deposit(userId: number, amountCents: number): number {
  if (amountCents <= 0) throw new Error("Monto inválido");
  db.prepare("UPDATE accounts SET balance_cents = balance_cents + ? WHERE user_id = ?").run(
    amountCents,
    userId
  );
  return getBalance(userId);
}

export function withdraw(userId: number, amountCents: number): number {
  const balance = getBalance(userId);
  if (amountCents <= 0) throw new Error("Monto inválido");
  if (balance < amountCents) throw new Error("Saldo insuficiente");
  db.prepare("UPDATE accounts SET balance_cents = balance_cents - ? WHERE user_id = ?").run(
    amountCents,
    userId
  );
  return getBalance(userId);
}

// ------- Inversiones (equivalente a tu invertir/verificar_inversion) -------
const INVEST_MATURITY_MS = 24 * 60 * 60 * 1000; // 24h reales; en Lua era 1 día MC

export function invest(userId: number, amountCents: number) {
  const balance = getBalance(userId);
  if (amountCents <= 0) throw new Error("Monto inválido");
  if (balance < amountCents) throw new Error("Saldo insuficiente");
  if (hasActiveInvestment(userId)) throw new Error("Ya tienes una inversión activa");

  db.prepare("UPDATE accounts SET balance_cents = balance_cents - ? WHERE user_id = ?").run(
    amountCents,
    userId
  );
  db.prepare(
    "INSERT INTO investments (user_id, amount_cents, started_at, matured) VALUES (?, ?, ?, 0)"
  ).run(userId, amountCents, Date.now());

  return { amountCents, startedAt: Date.now() };
}

export function hasActiveInvestment(userId: number): boolean {
  const row = db
    .prepare("SELECT id FROM investments WHERE user_id = ? AND matured = 0")
    .get(userId);
  return Boolean(row);
}

export function checkInvestment(userId: number) {
  const inv = db
    .prepare("SELECT * FROM investments WHERE user_id = ? AND matured = 0 ORDER BY id DESC LIMIT 1")
    .get(userId) as
    | { id: number; amount_cents: number; started_at: number }
    | undefined;

  if (!inv) return { status: "none" as const };

  const elapsed = Date.now() - inv.started_at;
  if (elapsed < INVEST_MATURITY_MS) {
    return {
      status: "pending" as const,
      remainingMs: INVEST_MATURITY_MS - elapsed,
      amountCents: inv.amount_cents,
    };
  }

  const total = Math.floor(inv.amount_cents * 1.1);
  const tx = db.transaction(() => {
    db.prepare("UPDATE accounts SET balance_cents = balance_cents + ? WHERE user_id = ?").run(
      total,
      userId
    );
    db.prepare("UPDATE investments SET matured = 1 WHERE id = ?").run(inv.id);
  });
  tx();

  return { status: "matured" as const, creditedCents: total, balanceCents: getBalance(userId) };
}

// ------- Cheques / facturas (equivalente a tu transferir y cobrar_cheque) -------
const BILL_TTL_MS = 2 * 24 * 60 * 60 * 1000; // 2 días

export function createBill(userId: number, amountCents: number): Bill {
  const code = crypto.randomBytes(12).toString("hex");
  const now = Date.now();
  const expires = now + BILL_TTL_MS;
  db.prepare(
    "INSERT INTO bills (code, user_id, amount_cents, created_at, expires_at) VALUES (?, ?, ?, ?, ?)"
  ).run(code, userId, amountCents, now, expires);
  // Descontamos al emisor (como en tu transferir: "te quita dinero")
  withdraw(userId, amountCents);
  return db.prepare("SELECT * FROM bills WHERE code = ?").get(code) as Bill;
}

export function redeemBill(redeemerId: number, code: string): number {
  const bill = db.prepare("SELECT * FROM bills WHERE code = ?").get(code) as Bill | undefined;
  if (!bill) throw new Error("Cheque no existe");
  if (bill.redeemed) throw new Error("Cheque ya cobrado");
  if (Date.now() > bill.expires_at) throw new Error("Cheque expirado");

  const tx = db.transaction(() => {
    db.prepare("UPDATE bills SET redeemed = 1 WHERE id = ?").run(bill.id);
    db.prepare("UPDATE accounts SET balance_cents = balance_cents + ? WHERE user_id = ?").run(
      bill.amount_cents,
      redeemerId
    );
  });
  tx();
  return bill.amount_cents;
}
// src/services/bankService.ts (añadir al final)

export interface BillSummary {
  id: number;
  code: string;
  amount_cents: number;
  redeemed: number;
  created_at: number;
  expires_at: number;
}

export function listMyBills(userId: number): BillSummary[] {
  return db
    .prepare(
      `SELECT id, code, amount_cents, redeemed, created_at, expires_at
       FROM bills WHERE user_id = ? ORDER BY id DESC`
    )
    .all(userId) as BillSummary[];
}

export function getBillById(userId: number, billId: number): BillSummary | undefined {
  return db
    .prepare(
      `SELECT id, code, amount_cents, redeemed, created_at, expires_at
       FROM bills WHERE id = ? AND user_id = ?`
    )
    .get(billId, userId) as BillSummary | undefined;
}

// ⚠️ Necesario para el middleware de propiedad: obtener el dueño SIN filtrar
export function getBillOwnerId(billId: number): number | undefined {
  const row = db.prepare("SELECT user_id FROM bills WHERE id = ?").get(billId) as
    | { user_id: number }
    | undefined;
  return row?.user_id;
}
