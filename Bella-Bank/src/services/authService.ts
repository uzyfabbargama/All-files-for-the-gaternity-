import bcrypt from "bcryptjs";
//import bcrypt from "bcrypt";
import crypto from "node:crypto";
import jwt from "jsonwebtoken";
import { db } from "../db/database.js";
import { env } from "../config/env.js";
import type { User, Role } from "../models/User.js";

export interface JwtPayload {
  id: number;
  username: string;
  role: Role;
}

export function hashPassword(plain: string): Promise<string> {
  return bcrypt.hash(plain, env.BCRYPT_ROUNDS);
}

export function verifyPassword(plain: string, hash: string): Promise<boolean> {
  return bcrypt.compare(plain, hash);
}

export function findByUsername(username: string): User | undefined {
  return db.prepare("SELECT * FROM users WHERE username = ?").get(username) as User | undefined;
}

export function findById(id: number): User | undefined {
  return db.prepare("SELECT * FROM users WHERE id = ?").get(id) as User | undefined;
}

export function createUser(username: string, passwordHash: string, role: Role = "USER"): User {
  const info = db
    .prepare("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)")
    .run(username, passwordHash, role);
  db.prepare("INSERT INTO accounts (user_id, balance_cents) VALUES (?, 0)").run(info.lastInsertRowid);
  return findById(Number(info.lastInsertRowid))!;
}

export function signAccessToken(user: User): string {
  const payload: JwtPayload = { id: user.id, username: user.username, role: user.role };
  return jwt.sign(payload, env.JWT_SECRET, { expiresIn: env.ACCESS_TOKEN_TTL as jwt.SignOptions["expiresIn"] });
}

export function signRefreshToken(user: User): string {
  const payload = { id: user.id };
  return jwt.sign(payload, env.JWT_REFRESH_SECRET, {
    expiresIn: env.REFRESH_TOKEN_TTL as jwt.SignOptions["expiresIn"],
  });
}

export function verifyRefreshToken(token: string): { id: number } {
  return jwt.verify(token, env.JWT_REFRESH_SECRET) as { id: number };
}

// Guardamos el refresh token hasheado (nunca en claro en BD)
export function storeRefreshToken(userId: number, token: string, ttlSeconds = 7 * 24 * 60 * 60): void {
  const tokenHash = crypto.createHash("sha256").update(token).digest("hex");
  const expiresAt = Math.floor(Date.now() / 1000) + ttlSeconds;
  db.prepare("INSERT INTO refresh_tokens (user_id, token_hash, expires_at) VALUES (?, ?, ?)").run(
    userId,
    tokenHash,
    expiresAt
  );
}

export function revokeRefreshToken(token: string): void {
  const tokenHash = crypto.createHash("sha256").update(token).digest("hex");
  db.prepare("UPDATE refresh_tokens SET revoked = 1 WHERE token_hash = ?").run(tokenHash);
}

export function isRefreshTokenValid(token: string): boolean {
  const tokenHash = crypto.createHash("sha256").update(token).digest("hex");
  const row = db
    .prepare("SELECT * FROM refresh_tokens WHERE token_hash = ? AND revoked = 0 AND expires_at > ?")
    .get(tokenHash, Math.floor(Date.now() / 1000));
  return Boolean(row);
}
