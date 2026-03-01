# --- Definición de tu número DZ ---
class DZ:
    def __init__(self, value):
        # Aseguramos que el valor sea numérico
        if not isinstance(value, (int, float)):
            raise TypeError("El valor de un número DZ debe ser numérico.")
        self.value = value # El 'N' en NDZ
    
    def __repr__(self):
        return f"{self.value}DZ"

    # Métodos para operaciones básicas
    # Estos se encargarán de cómo un objeto DZ interactúa con otros números/DZ
    
    # DZ * other
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                return self.value # Regla: DZ * 0 = N (restitución)
            elif other == 1:
                return 0 # Regla: DZ * 1 = 0 (anulación)
            else:
                return DZ(self.value * other) # Regla: NDZ * M = (N*M)DZ
        elif isinstance(other, DZ):
            return DZ(self.value * other.value) # Regla: NDZ1 * NDZ2 = (N1*N2)DZ
        else:
            return NotImplemented # Indica a Python que no sabe cómo manejar esta operación

    # other * DZ (para conmutatividad)
    def __rmul__(self, other):
        return self.__mul__(other)

    # DZ + other
    def __add__(self, other):
        if isinstance(other, DZ):
            return self.value + other.value # DZ1 + DZ2 = N1 + N2
        elif isinstance(other, (int, float)):
            return self.value + other # DZ + N = N_dz + N_normal
        return NotImplemented

    # other + DZ
    def __radd__(self, other):
        return self.__add__(other)

    # DZ - other
    def __sub__(self, other):
        if isinstance(other, DZ):
            return self.value - other.value
        elif isinstance(other, (int, float)):
            return self.value - other
        return NotImplemented

    # other - DZ
    def __rsub__(self, other):
        # rsub es especial: (other - self). Aquí el orden importa.
        if isinstance(other, (int, float)):
            return other - self.value
        return NotImplemented
    
    # DZ / other
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                # Este caso ya se maneja en la función operar para N/0
                return NotImplemented 
            return self.value / other
        elif isinstance(other, DZ):
            # Asumimos división de valores subyacentes
            if other.value == 0:
                 return NotImplemented # Evitar división por cero de otro DZ
            return self.value / other.value
        return NotImplemented

    # other / DZ
    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            if self.value == 0: # Si el DZ es 0DZ, entonces tenemos N/0DZ, que es N/0
                 return NotImplemented # Esto debería ser manejado por la función operar
            return other / self.value
        return NotImplemented


# --- Clase para el ZDZ, que encapsula la lógica de 0/0 ---
class ZDZ:
    def __init__(self, rules=None):
        self.rules = rules if rules is not None else {}
    
    def __repr__(self):
        return "ZDZ (singularidad emergente)"

    def process(self, input_data):
        print(f"Procesando {input_data} con ZDZ rules: {self.rules}")
        return f"Processed_by_ZDZ({input_data})"

# --- Función principal de la calculadora ---
def calculadora_zeroniana():
    print("¡Bienvenido a la Calculadora Zeroniana!")
    print("Ingresa tus operaciones. Escribe 'salir' para terminar.")
    print("Puedes usar números normales (ej. 5, 3.14) o crear números DZ (ej. DZ(7)).")
    print("Operadores soportados: +, -, *, /")
    print("Reglas especiales: N/0 creará un DZ, DZ * 0 = N, DZ * 1 = 0")

    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == 'salir':
                break

            # Intentar evaluar la expresión. Esto permite usar DZ(x) directamente
            # PELIGRO: eval() puede ser un riesgo de seguridad si el input no es confiable.
            # Para este ejercicio educativo, está bien.
            
            # Reemplazar "DZ(" por la clase DZ para que eval lo reconozca
            processed_input = user_input.replace("DZ(", "DZ(") 
            
            # Separar la expresión en partes para identificar los operandos y el operador
            parts = processed_input.split()
            
            if len(parts) != 3:
                print("Formato incorrecto. Usa 'operando1 operador operando2' (ej. 5 + 3, DZ(10) * 2).")
                continue

            # Convertir las partes a números o objetos DZ
            # Usamos eval() para manejar la creación de objetos DZ si el usuario los escribe como DZ(N)
            try:
                num_b_str, operador, num_a_str = parts
                num_b = eval(num_b_str, {'DZ': DZ}) # Aseguramos que 'DZ' sea reconocido por eval
                num_a = eval(num_a_str, {'DZ': DZ})
            except NameError:
                print("Error: Asegúrate de usar números válidos o el formato DZ(valor).")
                continue
            except Exception as e:
                print(f"Error al interpretar los números: {e}")
                continue

            # --- Lógica de la Zerevolution ---
            if operador == '/':
                if num_a == 0: # num_a es el divisor
                    if num_b == 0:
                        print("Resultado: ZDZ (singularidad emergente - 0/0, lógica en desarrollo)")
                        continue # No retornamos un objeto ZDZ aquí para la simplicidad del bucle
                    else:
                        # N / 0: Creamos un número DZ
                        valor_n = num_b.value if isinstance(num_b, DZ) else num_b
                        resultado = DZ(valor_n)
                        print(f"Resultado: {resultado}")
                else:
                    # División normal o con objetos DZ
                    try:
                        resultado = num_b / num_a
                        print(f"Resultado: {resultado}")
                    except TypeError:
                        print(f"Error: División no definida entre {type(num_b)} y {type(num_a)} en este contexto.")
                    except ZeroDivisionError:
                        print("Error: División por cero (no es 0/0, ni N/0).")
                    except Exception as e:
                        print(f"Error inesperado en división: {e}")
            elif operador == '*':
                try:
                    resultado = num_b * num_a
                    print(f"Resultado: {resultado}")
                except TypeError:
                    print(f"Error: Multiplicación no definida entre {type(num_b)} y {type(num_a)}.")
            elif operador == '+':
                try:
                    resultado = num_b + num_a
                    print(f"Resultado: {resultado}")
                except TypeError:
                    print(f"Error: Suma no definida entre {type(num_b)} y {type(num_a)}.")
            elif operador == '-':
                try:
                    resultado = num_b - num_a
                    print(f"Resultado: {resultado}")
                except TypeError:
                    print(f"Error: Resta no definida entre {type(num_b)} y {type(num_a)}.")
            else:
                print("Operador no soportado. Usa +, -, *, /")

        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")

# Iniciar la calculadora
calculadora_zeroniana()