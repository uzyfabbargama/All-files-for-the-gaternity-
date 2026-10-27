import dotenv from "dotenv";
dotenv.config();

function required(name: string): string {
  const val = process.env[name];
  if (!val) throw new Error(`Falta la variable de entorno ${name}`);
  return val;
}

export const env = {
  PORT: Number(process.env.PORT ?? 3000),
  JWT_SECRET: required("JWT_SECRET"),
  JWT_REFRESH_SECRET: required("JWT_REFRESH_SECRET"),
  ACCESS_TOKEN_TTL: process.env.ACCESS_TOKEN_TTL ?? "15m",
  REFRESH_TOKEN_TTL: process.env.REFRESH_TOKEN_TTL ?? "7d",
  BCRYPT_ROUNDS: Number(process.env.BCRYPT_ROUNDS ?? 12),
  DB_PATH: process.env.DB_PATH ?? "./bella-bank.db",
};
