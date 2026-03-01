from lark import Lark
from lark import Transformer
grammar = r"""
    // ---- REGLAS DE ESTRUCTURA PRINCIPALES ----
    start: assignment+

    // Ejemplo: Agente = ( ... )
    assignment: NAME "=" object_definition

    // Ejemplo: (Total(10), control_energia{...}, ...)
    object_definition: "(" (element ("," element)*)? ")"

    element: variable_declaration | controller_declaration_string | controller_declaration_number

    // ---- REGLAS PARA SLOTS Y CONTROLADORES ----
    // Ejemplo: Total(10) O calor(100)
    variable_declaration: NAME "(" NUMBER ("," STRING)? ")"

    // Ejemplo: control_energía{1, total += "Se ha acabado la energía"}
    controller_declaration_string: NAME "{" NUMBER "," operation ("," STRING)? "}"
    controller_declaration_number: NAME "{" NUMBER "," operation ("," NUMBER)? "}"
    // ---- REGLAS DE OPERACIÓN (El cuerpo del controlador) ----
    // Simplificado a una operación de asignación/modificación
    operation: NAME "+=" value | NAME "*=" value

    value: NUMBER | STRING | NAME

    // ---- TERMINALES (TOKENS) ----
    NAME: /[a-zA-Z_]\w*/
    NUMBER: /\d+(\.\d+)?/
    STRING: /"[^"]*"/ // Cadenas de texto
    // Ignorar espacios y comentarios
    %ignore /\s+/
    %ignore /#[^\n]*/
"""

# Inicializa el parser
parser = Lark(grammar)

class NTransformer(Transformer):
    # La raíz del programa
    start = list

    # Transforma una asignación (Agente = ...) en una tupla (nombre, definicion_objeto)
    def assignment(self, items):
        name = items[0].value
        definition = items[1]
        return (name, definition)

    # Transforma la lista de elementos dentro de los paréntesis en una lista
    def object_definition(self, items):
        return items

    # Convierte una variable de slot a un formato simple (NAME, VALOR, MENSAJE)
    def variable_declaration(self, items):
        name = items[0].value
        value = float(items[1]) # Convertimos el número a float/int
        message = items[2].strip('"') if len(items) > 2 else None
        return ('VAR_SLOT', name, value, message)

    # Convierte un controlador a (NAME, FACTOR, OPERACION, MENSAJE)
    def _transform_controller(self, items):
        # Lógica común de transformación para ambos tipos de controlador
        name = items[0].value
        factor = int(items[1])
        operation = items[2] 
        # Aquí puedes añadir la lógica para manejar el mensaje (items[3]) si existe,
        # ya sea STRING o NUMBER, asegurándote de manejar IndexError si falta.
        message = items[3].value.strip('"') if len(items) > 3 and items[3] else None

        return ('CONTROL', name, factor, operation, message)
    def controller_declaration_string(self, items):
        return self._transform_controller(items)

    def controller_declaration_number(self, items):
        return self._transform_controller(items)
    # Simplifica la operación (ej: total += "Se ha acabado la energía")
    def operation(self, items):
        var_name = items[0].value
        op = items[1].data  # El operador (+ ó *)
        val_token = items[2] # El token que puede ser NAME, NUMBER, o STRING

        if val_token.type == 'STRING':
            # Si es una cadena (ej. un mensaje de error)
            val = val_token.strip('"')
        elif val_token.type == 'NUMBER':
            # Si es un número
            val = float(val_token)
        elif val_token.type == 'NAME':
            # Si es otra variable (ej. 'total' o 'espada')
            val = val_token.value
        else:
            # Esto debería capturar cualquier caso inesperado, pero es poco probable con la gramática actual
            val = str(val_token) 

        return (op, var_name, val)
        # Métodos para limpiar los tokens
    def NAME(self, token): return token
    def NUMBER(self, token): return token
    def STRING(self, token): return token.value

code = """
Agente = (
    Total(10, "Alerta de Problema"),
    control_energía{1, total += "Se ha acabado la energía"},
    batería(100),
    consumo(1)
)
"""

tree = parser.parse(code)
# print(tree.pretty()) # Descomenta para ver el AST completo

# Transforma el AST en la estructura de datos que tu traductor Python necesita
n_data_structure = NTransformer().transform(tree)

print("\n--- Estructura de Datos para el Traductor N ---")
for obj_name, definition in n_data_structure:
    print(f"\nObjeto: {obj_name}")
    for element in definition:
        print(f"  {element}")