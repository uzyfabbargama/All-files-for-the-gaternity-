local xorid = require("xorid_api")

print("--- TEST DE SISTEMA XIP ---")
io.write("Usuario: ")
local user = io.read()
local id = xorid.generar(user)

print("Resultado para '" .. user .. "' es: " .. id)
