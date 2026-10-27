math.randomseed(os.time()) -- Usa el tiempo del juego como semilla
-- En algunas versiones de Lua se recomienda "quemar" el primer numero
_G.ID = math.random() 

--guardar_api
function guardar_archivo_xrp(nombre_real, u_id, p_id, saldo, invert)
    -- Constantes de tu terminal
    local K_USER = 15386
    local K_PASS = 102846
    local K_SALDO = 3678
    local K_INVERT = 6888
    local K_SEP = 156 -- El ::
    local K_FIN = 232 -- El ,,

    local ruta = "home/Users/" .. nombre_real .. ".xrp"
    local file = fs.open(ruta, "w")
    
    -- Trituramos la información
    file.writeLine(K_USER .. K_SEP .. u_id .. K_FIN)
    file.writeLine(K_PASS .. K_SEP .. p_id .. K_FIN)
    file.writeLine(K_SALDO .. K_SEP .. bit32.bnot(saldo) .. K_FIN)
    file.writeLine(K_INVERT .. K_SEP .. invert .. K_FIN)
    
    file.close()
    print("\n[!] Datos triturados y guardados en " .. nombre_real .. ".xrp")
end



--cargador_API
function cargar_archivo_xrp(nombre_real)
    -- Tus constantes del triturador
    local K_USER = "15386"
    local K_PASS = "102846"
    local K_SALDO = "3678"
    local K_INVERT = "6888"
    local K_SEP = "156"
    local K_FIN = "232"

    local ruta = "home/Users/" .. nombre_real .. ".xrp"
    
    if not fs.exists(ruta) then
        return nil, "La cuenta no existe en la base de datos."
    end

    local file = fs.open(ruta, "r")
    local datos = {}
    
    local linea = file.readLine()
    while linea do
        -- Buscamos qué etiqueta es (los primeros dígitos antes del separador)
        if linea:find("^" .. K_USER) then
            -- Extraemos lo que hay entre 156 y 232
            datos.u_id = tonumber(linea:match(K_SEP .. "(%d+)" .. K_FIN))
        elseif linea:find("^" .. K_PASS) then
            datos.p_id = tonumber(linea:match(K_SEP .. "(%d+)" .. K_FIN))
        elseif linea:find("^" .. K_SALDO) then
            local saldo_inv = tonumber(linea:match(K_SEP .. "(%d+)" .. K_FIN))
            datos.saldo = bit32.bnot(saldo_inv) -- ¡Lo regresamos a la vida!
        elseif linea:find("^" .. K_INVERT) then
            datos.invert = tonumber(linea:match(K_SEP .. "(%d+)" .. K_FIN))
        end
        linea = file.readLine()
    end
    file.close()
    
    return datos
end






--option_api
-- Al principio del programa
_G.dinero = bit32.bnot(0) -- Empezamos en 0 invertido
_G.tiempo_hecho = 0
_G.contrasenia_actual = "" -- Deberías asignarla al loguear
_G.monto_invertido = 0
function options(option)
  if verificar_dinero() then
    local acciones = {
      ["1"] = ver_saldo,
      ["2"] = depositar,
      ["3"] = invertir,
      ["4"] = cambiar_pass,
      ["5"] = transferir,
      ["6"] = verificar_inversion
    }

    if acciones[option] then
      acciones[option]()
    else
      print("Error: Esa opcion es invalida")
    end -- Aquí cerramos la validación de la opción seleccionada

  else 
    -- Este else pertenece al 'if verificar_dinero()'
    print("Tu cuenta ha sido corrupta, se ha anulado toda transaccion")
  end 
end

function verificar_dinero()
  local valit = _G.dinero
  local check = bit32.rshift(valit, 28)
  if check == 15 then
  	return true
  else
    print("saldo inválido/corrupto")
    return false
  	end
end
function ver_saldo()
  local valit = _G.dinero
  -- Tu validación pro:
  local check = bit32.rshift(valit, 28) 
  -- Nota: bnot de 0 en 32 bits es FFFFFFFF, por eso el rshift da 15 (F)
  if check == 15 then
  	local saldo_humano = bit32.bnot(_G.dinero)
  	print("Dinero: ", saldo_humano)
  	return saldo_humano
  else
    print("saldo inválido/corrupto")
    return
  	end
end
function isnil(var)
  if var == nil then
    return 0
  else
    return var
  end
end
function depositar()      
    write("Cantidad: ")
    local cant = read()
    cant = isnil(cant)
  write("Identificador de transaccion: ")
  local id_trans = read()
  id_trans = isnil(id_trans)
  write("Token de validacion: ")
  local token_usuario = tonumber(read())
  token_usuario = isnil(token_usuario)
  write("Hora: ")
  local tiempo = tonumber(read())
  tiempo = isnil(tiempo) 
  local tiempo_global = os.day() --JAJA, una variable local, de nombre global, es una variable loca
  if tiempo_global - tiempo >= 2 then
    print("ERROR: Tiempo expirado/dinero perdido")
    return -- Salimos si no es el tiempo correcto
  end
  -- Generamos el desafio internamente: "100.5"
  local desafio = cant .. "." .. id_trans .. "." .. tiempo
  local token_esperado = xorid(desafio) -- Tu funcion XORID

  if token_usuario == token_esperado then
    -- Convertimos a numero y quitamos el decimal "fantasma"
    local valor_real = math.floor(tonumber(cant))
    _G.dinero = bit32.bnot(bit32.bnot(_G.dinero) + valor_real)
    print("Transaccion exitosa. Se han sumado " .. valor_real .. " credits.")
  else
    print("ERROR: El token no coincide con el desafio generado.")
  end
end
function verificar_inversion()
  print("\n--- Consultando Mercado de Valores ---")
  
  if not _G.monto_invertido or _G.monto_invertido == 0 then
    print("No tienes inversiones activas.")
    return
  end

  local tiempo_actual = os.time()
  -- Si el tiempo actual es menor al inicial, significa que paso la medianoche (24:00)
  -- o simplemente comparamos si la diferencia es suficiente para un ciclo.
  
  -- En Minecraft, si tiempo_actual < tiempo_hecho, es que ya paso un dia.
  if tiempo_actual < _G.tiempo_hecho then
    print("¡Felicidades! Tu inversion ha madurado.")
    
    local amount = _G.monto_invertido
    -- Aplicamos el 10% de transurgencia
    amount = amount + (amount * 0.1)
    
    -- Actualizamos los globales (quitamos el decimal con floor)
    _G.monto_invertido = math.floor(amount)
    
    -- Devolvemos el dinero al saldo principal triturado
    local saldo_actual = bit32.bnot(_G.dinero)
    _G.dinero = bit32.bnot(saldo_actual + _G.monto_invertido)
    
    -- Reseteamos la inversion para que no se cobre infinitas veces
    _G.monto_invertido = 0
    _G.tiempo_hecho = 0
    
    print("Nuevo monto acreditado: ", amount)
    -- Guardamos automaticamente para que no haya "tricks" de reinicio
    guardar_archivo_xrp(_G.nombre_usuario, _G.u_id_global, _G.p_id_global, bit32.bnot(_G.dinero), 0)
  else
    print("La inversion sigue procesandose...")
    print("Tiempo restante estimado: ", math.floor(_G.tiempo_hecho - tiempo_actual), " unidades.")
  end
end

function invertir()
  print("Bienvenido al fondo de inversion de BellaBank")
  write("Password: ")
  local pass = read("*")
  pass = xorid(pass)
  -- Aqui deberías comparar con la pass real del login
  if _G.contrasenia_actual == pass then
    print("\nCorrecto")
  else
    print("\nIncorrecto")
    return
  end
  write("Cuanto quiere colocar: ")
  local amount = tonumber(read())
  _G.dinero = bit32.bnot(bit32.bnot(_G.dinero) - amount)
  _G.tiempo_hecho = os.time()
  _G.monto_invertido = amount
  print("Inversion realizada. Espere 24 horas de MC.")
end
function transferir()
  print("Bienvenido al modo transferencia, por ahora no está disponible para transferir de forma automática a otro usuario, pero te quita _G.dinero, que puedes intercambiar por un item")
  write("Coloque su contraseña: ")
  local pass = read("*")
  pass = xorid(pass)
  if (pass == _G.contrasenia_actual) then
     print("\nContraseña correcta")
  else
     print("\nContraseña incorrecta, inténtalo de nuevo")
     return
  end
  write("Cuanto quiere gastar: ")
  local amount = tonumber(read())
  local total = bit32.bnot(_G.dinero)
  print(total)
  if (total + amount >= 0) then
    print("\nGasto inteligente, no te quedarás con menor a 0")
    print(total)
    _G.dinero = _G.dinero + amount -- hay que invertir, suma es resta jaja
    write("nombre tu transacción:")
    local name = read()
    print("\n")
    local ruta = "home/Transac/" .. name .. ".bill"
    local file = fs.open(ruta, "w")
    local tiempo = os.day()
    local desafio = amount .. "." .. _G.ID .. "." .. tiempo
    local desafio = xorid(desafio)
    file.writeLine("Cheque: " .. amount)
    file.writeLine("ID: " .. _G.ID)
    file.writeLine("Token: " .. desafio)
    file.writeLine("Hora: " .. tiempo)
    file.writeLine("---TIEMPO LÍMITE 2 DIAS MC---")
    _G.ID = math.random()
    file.close()
  else
    print("\nError, no puedes tener _G.dinero negativo")
    return
  end
end
function cambiar_pass()
  print("Cambie su contrasenia seguido, para que no le roben sus datos, juejuejue")
  write("Contrasenia anterior: ")
  local bef_pass = read("1")
  bef_pass = xorid(bef_pass)
  if bef_pass == _G.contrasenia_actual then
    print("\nContrasenia reconocida")
  else
    print("\nContrasenia incorrecta")
    return
  end
  write("Nueva contrasenia: ")
  local new_pass = read("2")
  _G.contrasenia_actual = new_pass
  _G.p_id_global = select(2, calcular_ID(_G.nombre_usuario, new_pass))
  guardar_archivo_xrp(_G.nombre_usuario, _G.u_id_global, _G.p_id_global, bit32.bnot(_G.dinero), 0)

end
-- xorid_api.lua
--xorid puro
function xorid(dato)
  local id_acumulado = 0 -- Hay que definirlo antes de empezar
  
  -- Bucle para el Usuario
  for i = 1, #dato do
    local caracter = dato:sub(i, i)
    local byte_val = string.byte(caracter)
    -- Aquí estaba el cálculo
    id_acumulado = bit32.lshift(bit32.bxor(id_acumulado, byte_val), 1)
  end
  local id_user = id_acumulado
  return id_acumulado
end
function calcular_ID(user, password)

  
  local id_acumulado = 0 -- Hay que definirlo antes de empezar
  
  -- Bucle para el Usuario
  for i = 1, #user do
    local caracter = user:sub(i, i)
    local byte_val = string.byte(caracter)
    -- Aquí estaba el cálculo
    id_acumulado = bit32.lshift(bit32.bxor(id_acumulado, byte_val), 1)
  end
  local id_user = id_acumulado
  
  id_acumulado = 0 -- ¡IMPORTANTE! Resetear para la contrasenia
  -- Bucle para la Contrasenia
  for i = 1, #password do
    local caracter = password:sub(i, i)
    local byte_val = string.byte(caracter)
    id_acumulado = bit32.lshift(bit32.bxor(id_acumulado, byte_val), 1)
  end
  local id_password = id_acumulado
  _G.contrasenia_actual = id_password
  --print("\nID Usuario: " .. id_user)
  --print("ID Password: " .. id_password)
  
  return id_user, id_password
end -- ¡No te olvides de este end!



-- banco.lua
print("--- SISTEMA BANCARIO ---")
-- MAIN LOOP (Para evitar el spaghetti)
print("--- BELLA BANK ---")
write("Usuario: ")
local user_in = read()
local datos = cargar_archivo_xrp(user_in)
 
if not datos then
    print("Cuenta nueva. Cree su password:")
    local p_in = read("*")
    local u_id, p_id = calcular_ID(user_in, p_in)
    _G.nombre_usuario = user_in
    _G.u_id_global = u_id
    _G.p_id_global = p_id
    _G.dinero = bit32.bnot(0)
    guardar_archivo_xrp(user_in, u_id, p_id, 0, 0)
else
    print("Bienvenido", user_in, "al BellaBank")
    write("Password: ")
    local p_test = read("*")
    local _, p_id_test = calcular_ID(user_in, p_test)
    if p_id_test == datos.p_id then
        _G.nombre_usuario = user_in
        _G.u_id_global = datos.u_id
        _G.p_id_global = datos.p_id
        _G.dinero = bit32.bnot(datos.saldo)
    else
        print("Acceso Denegado.") return
    end
end

-- El Bucle del Menú
while true do
	write("___") --para que el humano pueda ver el resultado, sino, no verá nada, jaja
	local mov = read()
    term.clear()
    term.setCursorPos(1,1)
    print("Bienvenido, " .. _G.nombre_usuario)
    print("1. Ver Saldo  2. Depositar  3. Invertir")
    print("4. CambiPass  5. Tienda     6. Verificar Inversión")
    print("7_ Salir")
    write("Opcion: ")
    local opt = read()
    -- EL GUARDADO FINAL ANTES DEL BREAK
        print("\n[!] Sincronizando datos con la base de datos XRP...")
        -- Recuperamos el saldo real (bnot del bnot) para guardarlo
        local saldo_para_guardar = bit32.bnot(_G.dinero)
    if opt == "7" then 
        guardar_archivo_xrp(
            _G.nombre_usuario, 
            _G.u_id_global, 
            _G.p_id_global, 
            saldo_para_guardar, 
            _G.monto_invertido
        )
        print("Sesion cerrada de forma segura. ¡Adios!")
        break 
    end
    
    options(opt)
end
