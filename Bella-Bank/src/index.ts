import express from "express";
import { env } from "./config/env.js";
import { authRoutes } from "./routes/authRoutes.js";
import { bankRoutes } from "./routes/bankRoutes.js";
import { shopRoutes } from "./routes/shopRoutes.js";
import { apiLimiter } from "./middleware/rateLimiter.js";

const app = express();
app.use(express.json({ limit: "16kb" }));
app.use(apiLimiter);

// CORS manual y restrictivo (nunca '*' en producción)
app.use((req, res, next) => {
  const allowed = ["http://localhost:5173", "http://localhost:3000"];
  const origin = req.headers.origin;
  if (origin && allowed.includes(origin)) res.setHeader("Access-Control-Allow-Origin", origin);
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS");
  if (req.method === "OPTIONS") return res.sendStatus(204);
  next();
});

app.use("/api/auth", authRoutes);
app.use("/api/bank", bankRoutes);
app.use("/api/shop", shopRoutes);

app.get("/health", (_req, res) => res.json({ status: "ok" }));

app.use((_req, res) => res.status(404).json({ error: "Ruta no encontrada" }));

app.listen(env.PORT, () => {
  console.log(`BellaBank API escuchando en http://localhost:${env.PORT}`);
});
