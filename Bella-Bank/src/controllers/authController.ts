import type { Request, Response } from "express";
import {
  createUser,
  findByUsername,
  hashPassword,
  revokeRefreshToken,
  signAccessToken,
  signRefreshToken,
  storeRefreshToken,
  verifyPassword,
  verifyRefreshToken,
  isRefreshTokenValid,
  findById,
} from "../services/authService.js";

export async function register(req: Request, res: Response) {
  const { username, password } = req.body as { username: string; password: string };
  if (findByUsername(username)) {
    return res.status(409).json({ error: "El usuario ya existe" });
  }
  const hash = await hashPassword(password);
  const user = createUser(username, hash);
  return res.status(201).json({ id: user.id, username: user.username, role: user.role });
}

export async function login(req: Request, res: Response) {
  const { username, password } = req.body as { username: string; password: string };
  const user = findByUsername(username);
  if (!user) return res.status(401).json({ error: "Credenciales inválidas" });

  const ok = await verifyPassword(password, user.password_hash);
  if (!ok) return res.status(401).json({ error: "Credenciales inválidas" });

  const accessToken = signAccessToken(user);
  const refreshToken = signRefreshToken(user);
  storeRefreshToken(user.id, refreshToken);

  return res.json({
    mensaje: "Inicio de sesión exitoso",
    accessToken,
    refreshToken,
    user: { id: user.id, username: user.username, role: user.role },
  });
}

export function refresh(req: Request, res: Response) {
  const { refreshToken } = req.body as { refreshToken?: string };
  if (!refreshToken) return res.status(400).json({ error: "Falta refreshToken" });

  if (!isRefreshTokenValid(refreshToken)) {
    return res.status(403).json({ error: "Refresh token inválido o revocado" });
  }

  try {
    const { id } = verifyRefreshToken(refreshToken);
    const user = findById(id);
    if (!user) return res.status(401).json({ error: "Usuario no existe" });
    const accessToken = signAccessToken(user);
    return res.json({ accessToken });
  } catch {
    return res.status(403).json({ error: "Refresh token expirado o inválido" });
  }
}

export function logout(req: Request, res: Response) {
  const { refreshToken } = req.body as { refreshToken?: string };
  if (refreshToken) revokeRefreshToken(refreshToken);
  return res.json({ mensaje: "Sesión cerrada" });
}
