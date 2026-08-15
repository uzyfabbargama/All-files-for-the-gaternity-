#!/usr/bin/env lua
local a = 10
local b = 5

local suma = a + b
local resta = a - b
local multi = a * b
local div = a / b
local modulo = a % b
local potencia = a ^ 2
local y = a & b
local o = a | b
local eo = a ~ b
local n_a = ~a
local n_b = ~b
local shl = a << b
local shr = a >> b
print("--- Resultados Aritméticos ---")
print("Suma:", suma, "Div:", div, "Mod:", modulo, "Pow:", potencia)

print("\n--- Resultados de Bits (Metal) ---")
print("AND:", y, "OR:", o, "XOR:", eo)
print("NOT A:", n_a, "SHL:", shl, "SHR:", shr)
