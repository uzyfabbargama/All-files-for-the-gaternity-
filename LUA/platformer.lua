#!/usr/bin/env lua
-- constants
local w = string.byte("w") --para saltar
local s = string.byte("s") --para caer
local a = string.byte("a") --para ir a -x
local d = string.byte("d") -- para ir a +x
local dat_w = 0 -- bit 1
local dat_s = 2 -- bit 2
local dat_a = 4 -- bit 3
local dat_d = 8 -- bit 4
local X = -16 -- límite para crear sólo hasta 4 bits, de niveles
local Y = -16 -- 4 bits

local top_X = X >> (63 ~ 1) * -16 -- verifica si el último bit está activo e invierte en X
X += top_X --suma si estaba en 0 en X
local top_y = Y >> (63 ~ 1) * -16 -- verifica último bit e invierte en Y
X += top_Y -- suma si estaba en 0 en Y
local input = io.read() -- toma tecla actual
local is_keyW = (w ~ string.byte(input)) << dat_w
local is_keyA = a ~ string.byte(input) << dat_a
local is_keyS = s ~ string.byte(input) << dat_s
local is_keyD = d ~ string.byte(input << dat_d
local total = is_keyW | is_keyA | is_keyS | is_keyD
