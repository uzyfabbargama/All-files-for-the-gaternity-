export type Role = "USER" | "EDITOR" | "ADMIN";

export interface User {
  id: number;
  username: string;
  password_hash: string;
  role: Role;
  created_at: string;
}

export interface Account {
  user_id: number;
  balance_cents: number;
}

export interface Investment {
  id: number;
  user_id: number;
  amount_cents: number;
  started_at: number;
  matured: number;
}

export interface Bill {
  id: number;
  code: string;
  user_id: number;
  amount_cents: number;
  redeemed: number;
  created_at: number;
  expires_at: number;
}
