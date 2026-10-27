import type { NextFunction, Request, Response } from "express";
import { z, ZodError, ZodSchema } from "zod";

export function validateBody(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (err) {
      if (err instanceof ZodError) {
        return res.status(400).json({ error: "Datos inválidos", detalles: err.issues });
      }
      next(err);
    }
  };
}

export const registerSchema = z.object({
  username: z.string().min(3).max(24).regex(/^[a-zA-Z0-9_]+$/, "Solo letras, números y _"),
  password: z.string().min(8).max(72),
});

export const loginSchema = registerSchema;

export const depositSchema = z.object({
  amountCents: z.number().int().positive().max(1_000_000_00),
});

export const investSchema = depositSchema;

export const transferSchema = z.object({
  amountCents: z.number().int().positive().max(1_000_000_00),
  concept: z.string().max(80).optional(),
});
