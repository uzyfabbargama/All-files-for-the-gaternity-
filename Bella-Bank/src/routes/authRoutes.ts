import { Router } from "express";
import { login, logout, refresh, register } from "../controllers/authController.js";
import { loginLimiter } from "../middleware/rateLimiter.js";
import { loginSchema, registerSchema, validateBody } from "../middleware/validate.js";

export const authRoutes = Router();

authRoutes.post("/register", validateBody(registerSchema), register);
authRoutes.post("/login", loginLimiter, validateBody(loginSchema), login);
authRoutes.post("/refresh", refresh);
authRoutes.post("/logout", logout);
