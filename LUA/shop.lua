  --print("¿Que desea hacer ahora?\n 1. Guardar/Crear \n 2. Salir\n 3. Vender\n 4. Comprar\n 5. Agregar_item")
math.randomseed(os.time()) -- Usa el tiempo del juego como semilla
-- En algunas versiones de Lua se recomienda "quemar" el primer numero
_G.ID = math.random() 
--options
function options(option)

    local acciones = {
      ["1"] = guardar_inventario,
      ["3"] = cobrar_cheque,
      ["4"] = comprar_item,
      ["5"] = additem,
    }

    if acciones[option] then
      acciones[option]()
    else
      print("Error: Esa opcion es invalida")
    end -- Aquí cerramos la validación de la opción seleccionada
end
function parser(nombre)
    local ruta = "home/Shop/" .. nombre .. ".ite"
    if not fs.exists(ruta) then
        return nil, "El ítem no existe en la base de datos"
    end
    
    local file = fs.open(ruta, "r")
    local contenido = file.readAll() -- Leemos todo el archivo de una vez
    file.close()
    
    local datos = {}
    -- Buscamos el patrón: (Cualquier cosa antes de ::) :: (Espacio opcional) (Dígitos) ,,
    for item, cantidad in string.gmatch(contenido, "([^:]+)::%s*(%d+),,") do
        -- Quitamos espacios sobrantes en el nombre si los hay
        local item_limpio = item:match("^%s*(.-)%s*$")
        datos[item_limpio] = tonumber(cantidad)
    end
    
    return datos
end

--calcular precios
function calcular_precios(tabla_datos)
    local variedades = 0
    for _ in pairs(tabla_datos) do variedades = variedades + 1 end
    
    local creditos_totales = variedades * 16
    local precios = {}

    print("\n--- ECONOMIA ACTUAL ---")
    print("Variedades: " .. variedades .. " | Creditos: " .. creditos_totales)
    print("-----------------------")

    for item, cantidad in pairs(tabla_datos) do
        -- Evitamos división por cero si la cantidad es 0
        local precio = 0
        if cantidad > 0 then
            -- math.ceil redondea hacia arriba como querías
            precio = math.ceil(creditos_totales / cantidad)
        end
        precios[item] = precio
        print(item .. ": " .. precio .. " credits (Stock: " .. cantidad .. ")")
    end
    
    return precios, creditos_totales
end

--comprar
function comprar_item()
    write("Nombre del archivo: ")
    local nombre_base = read
    local inventario = parser(nombre_base)
    if not inventario then return end
    
    local precios = calcular_precios(inventario)
    
    write("\n¿Qué deseas comprar?: ")
    local item = read()
    
    if not inventario[item] or inventario[item] <= 0 then
        print("No hay stock de " .. item)
        return
    end

    local precio = precios[item]
    
    -- La tienda genera un ID único para esta transacción
    local trans_id = _G.ID
    local nombre_ticket = "pago_" .. item .. "_" .. trans_id
    
    -- Generamos el archivo de cobro que el usuario debe llevar al banco
    local ruta = "home/Users/" .. nombre_ticket .. ".bill"
    local file = fs.open(ruta, "w")
    
    -- Usamos xorid para que el banco sepa que es un cobro legítimo de la TIENDA
    local desafio = precio .. "." .. trans_id
    local token = xorid(desafio)
    
    file.writeLine("Cheque: " .. precio)
    file.writeLine("ID: " .. trans_id)
    file.writeLine("Token: " .. token)
    file.close()
    _G.ID = math.random()
    -- Restamos el stock de la tienda (el ítem queda reservado o entregado)
    inventario[item] = inventario[item] - 1
    guardar_inventario(nombre_base, inventario)

    print("\n[!] Factura generada: " .. nombre_ticket .. ".bill")
    print("Por favor, procesa este archivo en el banco para completar el pago de " .. precio .. " credits.")
end


--vender
function cobrar_cheque(nombre_bill)
    local ruta = "home/Users/" .. nombre_bill .. ".bill"
    if not fs.exists(ruta) then return nil, "El cheque no existe" end

    local file = fs.open(ruta, "r")
    local monto = tonumber(file.readLine():match("Cheque: (%d+)"))
    local id_original = file.readLine():match("ID: (.+)")
    local token_recibido = tonumber(file.readLine():match("Token: (%d+)"))
    file.close()

    -- El desafío se reconstruye igual que en transferir()
    local desafio = monto .. "." .. id_original
    if xorid(desafio) == token_recibido then
        -- Sumamos al saldo global triturado
        local saldo_actual = bit32.bnot(_G.dinero)
        _G.dinero = bit32.bnot(saldo_actual + monto)
        fs.delete(ruta) -- ¡Importante! Destruir el cheque para que no se reuse
        return monto
    else
        return nil, "Fraude detectado: Token inválido"
    end
end

--xorid
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

-- calcular precios
function additem()
    term.clear()
    print("--- GESTION DE MATERIALES ---")
    write("Nombra la cuenta (archivo): ")
    local nombre_archivo = read()

    -- CARGA PREVIA: Intentamos leer si ya existe el archivo
    local tabla, err = parser(nombre_archivo)
    if not tabla then
        print("[!] Creando nueva cuenta...")
        tabla = {}
    else
        print("[!] Cuenta cargada. Agregando nuevos items...")
    end

    while true do
        write("\nItem: ")
        local item = read()
        write("Cantidad: ")
        local cant = tonumber(read()) or 0
        
        tabla[item] = (tabla[item] or 0) + cant
        
        write("¿Agregar otro? (s/n): ")
        if read():lower() == "n" then break end
    end

    guardar_inventario(nombre_archivo, tabla)
end


--función para guardar
function guardar_inventario(nombre, tabla_datos)
    local ruta = "home/Shop/" .. nombre .. ".ite"
    local file = fs.open(ruta, "w")
    
    local str = ""
    for item, cant in pairs(tabla_datos) do
        str = str .. item .. ":: " .. cant .. ",, "
    end
    
    file.write(str)
    file.close()
end

--función de agregar ítem
function additem()
    term.clear()
    print("--- GESTION DE MATERIALES ---")
    write("Nombra la cuenta (archivo): ")
    local nombre_archivo = read()

    -- CARGA PREVIA: Intentamos leer si ya existe el archivo
    local tabla, err = parser(nombre_archivo)
    if not tabla then
        print("[!] Creando nueva cuenta...")
        tabla = {}
    else
        print("[!] Cuenta cargada. Agregando nuevos items...")
    end

    while true do
        write("\nItem: ")
        local item = read()
        write("Cantidad: ")
        local cant = tonumber(read()) or 0
        
        tabla[item] = (tabla[item] or 0) + cant
        
        write("¿Agregar otro? (s/n): ")
        if read():lower() == "n" then break end
    end

    guardar_inventario(nombre_archivo, tabla)
end

while true do
  local mov = read()
  term.clear()
  term.setCursorPos(1,1)
  print("Bienvenido a la tienda")
  print("---GESTION DE RECURSOS Y PRECIOS ---")
--  additem()
  print("¿Que desea hacer ahora?\n 1. Guardar/Crear \n 2. Salir\n 3. Vender\n 4. Comprar\n 5. Agregar_item")
  local opt = read()
  options(opt)
  if opt == "2" then 
  break 
  end
end
