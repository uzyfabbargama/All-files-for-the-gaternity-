import { db } from "../db/database.js";
import { createBill } from "./bankService.js";

export function getCatalog() {
  return db.prepare("SELECT id, name, stock, price FROM shop_items").all();
}

export function addOrRestock(name: string, stock: number, price: number) {
  db.prepare(
    `INSERT INTO shop_items (name, stock, price) VALUES (?, ?, ?)
     ON CONFLICT(name) DO UPDATE SET stock = stock + excluded.stock, price = excluded.price`
  ).run(name, stock, price);
}

export function purchaseItem(userId: number, itemName: string) {
  const item = db.prepare("SELECT * FROM shop_items WHERE name = ?").get(itemName) as
    | { id: number; name: string; stock: number; price: number }
    | undefined;

  if (!item) throw new Error("Ítem no existe");
  if (item.stock <= 0) throw new Error("Sin stock");

  const tx = db.transaction(() => {
    db.prepare("UPDATE shop_items SET stock = stock - 1 WHERE id = ?").run(item.id);
    // Generamos la factura (el usuario deberá pagarla con redeemBill)
    return createBill(userId, item.price);
  });

  return tx();
}
