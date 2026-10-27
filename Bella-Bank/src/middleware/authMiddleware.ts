import type { NextFunction, Request, Response } from "express";
import jwt from "jsonwebtoken";
import { env } from "../config/env.js";
import type { JwtPayload } from "../services/authService.js";
import type { Role } from "../models/User.js";

export interface AuthRequest extends Request {
  user?: JwtPayload;
}

export function verificarToken(req: AuthRequest, res: Response, next: NextFunction) {
  const header = req.headers["authorization"];
  const token = header && header.split(" ")[1];
  if (!token) return res.status(401).json({ error: "Acceso denegado. No se proporcionó token." });

  try {
    const payload = jwt.verify(token, env.JWT_SECRET) as JwtPayload;
    req.user = payload;
    next();
  } catch {
    return res.status(403).json({ error: "Token inválido o expirado." });
  }
}

export function requerirRol(rolesPermitidos: Role[]) {
  return (req: AuthRequest, res: Response, next: NextFunction) => {
    if (!req.user || !rolesPermitidos.includes(req.user.role)) {
      return res.status(403).json({ error: "No tienes los permisos necesarios." });
    }
    next();
  };
}

// Autorización por propiedad (previene IDOR)
export function esPropietario(getOwnerId: (req: AuthRequest) => number | undefined) {
  return (req: AuthRequest, res: Response, next: NextFunction) => {
    if (req.user?.role === "ADMIN") return next();
    const ownerId = getOwnerId(req);
    if (ownerId === undefined || ownerId !== req.user?.id) {
      return res.status(403).json({ error: "No tienes permiso sobre este recurso." });
    }
    next();
  };
}
