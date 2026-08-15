local M = {}

function M.generar(palabra)
    local id = 0
    for i = 1, #palabra do
        local byte_val = string.byte(palabra:sub(i, i))
        -- En Linux usamos el operador << 1 o * 2
        id = ((id ~ byte_val) * 2) 
    end
    return id
end

return M
