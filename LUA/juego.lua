#!/usr/bin/env lua

print("Escribe algo (Lubuntu/Python/Assembler):")

-- io.read() lee una línea completa del teclado
local entrada = io.read()

local respuestas = {
    ["Lubuntu"] = "¡El SO más ligero y eficiente!",
    ["Python"] = "Gran abstracción, pero Lua es más rápido.",
    ["Assembler"] = "Directo al metal. Respetos."
}

-- Si la entrada no está en la tabla, devolverá 'nil' (nulo)
-- Usamos el truco del 'or' para dar una respuesta por defecto sin IF
local mensaje = respuestas[entrada] or "No reconozco esa realidad, pero suena interesante."

print(mensaje)
