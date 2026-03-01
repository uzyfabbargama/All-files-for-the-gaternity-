import re

# --- Definición de tu número DZ ---
class DZ:
    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("El valor de un número DZ debe ser numérico.")
        self.value = value
    
    def __repr__(self):
        return f"{self.value}DZ"

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                return self.value 
            elif other == 1:
                return 0 # Regla: DZ * 1 = 0 (anulación)
            else:
                return DZ(self.value * other) 
        elif isinstance(other, DZ):
            return DZ(self.value * other.value)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        if isinstance(other, DZ):
            return self.value + other.value
        elif isinstance(other, (int, float)):
            return self.value + other
        return NotImplemented

    # (omitimos __radd__, __sub__, __rsub__ para brevedad, pero se implementarían igual)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                return NotImplemented
            return self.value / other
        elif isinstance(other, DZ):
            if other.value == 0:
                 return NotImplemented
            return self.value / other.value
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            if self.value == 0:
                 return NotImplemented
            return other / self.value
        return NotImplemented

# --- Clase para el ZDZ, el "procesador" de la singularidad 0/0 ---
class ZDZ:
    def __init__(self, quantums=None):
        # Si no se dan quantums, usamos los predeterminados (tu simetría del 7)
        self.quantums = quantums if quantums else {
            1: (6, 6, 1),
            2: (5, 5, 2),
            3: (4, 4, 3),
            4: (3, 3, 4),
            5: (2, 2, 5),
            6: (1, 1, 6)
        }
    
    def __repr__(self):
        return "ZDZ_Activo (Onda de Singularidad)"

    def parse_quantums(self, quant_string):
        """
        Parsea la cadena de quantums dada por el usuario y la convierte en un diccionario.
        Ejemplo: "Quant (1 = 3, 4 = 6, 7 = 3)" -> {1: (3, 3, 1), 4: (6, 6, 4), 7: (3, 3, 7)}
        """
        quant_dict = {}
        # Usamos regex para extraer los pares N=N'
        matches = re.findall(r'(\d+)\s*=\s*(\d+)', quant_string)
        for n1, n2 in matches:
            n1, n2 = int(n1), int(n2)
            quant_dict[n1] = (n2, n2, n1) # (Y, X_pareja, Y_pareja)
        return quant_dict

    def transform_point(self, x_in):
        """
        Transforma un punto X usando las reglas de los quantums.
        """
        # Intentar encontrar la regla de transformación en los quantums definidos
        y_in = x_in # Por defecto, Y es igual a X
        x_out = x_in # Valor por defecto si no hay regla directa
        y_out = y_in # Valor por defecto

        if x_in in self.quantums:
            # Si x_in es una clave (ej. X1), su pareja X_out es el segundo elemento de la tupla
            x_out = self.quantums[x_in][1]
            y_partner_in_quant = self.quantums[x_in][0] # El Y asociado con X_in en la regla
            if y_partner_in_quant != 0:
                proportion = y_in / y_partner_in_quant
                if proportion < 1:
                    y_out = y_in - proportion
                else:
                    y_out = y_in + proportion
            else:
                y_out = y_in # Mantener Y si la proporción no se puede calcular
        else:
            # Lógica de Extrapolación (para números fuera de los quantums directos)
            # Buscamos el quantum más cercano o una relación de escala
            found_rule = False
            for q_x_in, q_vals in self.quantums.items():
                q_y_in = q_vals[0]
                q_x_out = q_vals[1]
                q_y_out = q_vals[2]

                if x_in % q_x_in == 0 and q_x_in != 0:
                    f = x_in / q_x_in
                    x_out = q_x_out * f
                    if q_y_out != 0:
                        y_out = y_in + (q_y_in / q_y_out) * f
                    else:
                        y_out = y_in
                    found_rule = True
                    break

            if not found_rule:
                # Si no se encuentra un múltiplo, aplicamos la regla de la menor distancia
                # Calculamos la distancia a cada X en los quantums
                distances = {q_x: abs(x_in - q_x) for q_x in self.quantums}
                closest_x = min(distances, key=distances.get)
                # Aplicamos la regla del quantum más cercano
                closest_y = self.quantums[closest_x][0]
                x_out = self.quantums[closest_x][1]

                # Para Y, intentamos mantener una proporción similar a la del quantum cercano
                if closest_y != 0:
                    y_out = y_in + (x_in / closest_x) * (closest_y / closest_x) # Adaptado para la nueva estructura
                else:
                    y_out = y_in # Si el Y del quantum cercano es 0, mantenemos Y

        return (x_out, y_out)

    def process_wave(self, initial_point_value, num_steps=10):
        """
        Simula la propagación de la "Onda de Singularidad" desde un punto inicial.
        """
        print(f"\n--- Generando Onda de Singularidad ZDZ desde el punto {initial_point_value} ---")
        wave_points = []
        for i in range(1, num_steps + 1):
            x_in = i # Usamos 'i' como el valor del punto actual para la onda
            x_out, y_out = self.transform_point(x_in)
            wave_points.append(f"(X{x_out:.3f}, Y{y_out:.3f})")
            print(f"Punto {i}: (X{x_in}, Y{x_in}) transformado a {wave_points[-1]}")
        print("\n--- Fin de la Onda de Singularidad ---")
        return wave_points

# --- Función principal de la calculadora ---
def calculadora_zeroniana():
    print("¡Bienvenido a la Calculadora Zeroniana!")
    print("Ingresa tus operaciones. Escribe 'salir' para terminar.")
    print("Puedes usar números normales (ej. 5, 3.14) o crear números DZ (ej. DZ(7)).")
    print("Operadores soportados: +, -, *, /")
    print("Reglas especiales de Zerevolution:")
    print(" - N/0 creará un NDZ (Número Dividido por Cero)")
    print(" - DZ(N) * 0 = N (Restitución)")
    print(" - DZ(N) * 1 = 0 (Anulación)")
    print(" - 0 / 0 invocará una 'Onda de Singularidad' ZDZ.")

    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == 'salir':
                break

            processed_input = re.sub(r'(\d+(\.\d+)?)DZ', r'DZ(\1)', user_input)
            parts = processed_input.split()
            
            if len(parts) != 3:
                print("Formato incorrecto. Usa 'operando1 operador operando2' (ej. 5 + 3, DZ(10) * 2).")
                continue

            try:
                num_b_str, operador, num_a_str = parts
                num_b = eval(num_b_str, {'DZ': DZ})
                num_a = eval(num_a_str, {'DZ': DZ})
            except (NameError, TypeError) as e:
                print(f"Error al interpretar los números: {e}. Asegúrate de usar números válidos o el formato DZ(valor).")
                continue
            except Exception as e:
                print(f"Error inesperado al interpretar los números: {e}")
                continue

            # --- Lógica de la Zerevolution ---
            if operador == '/':
                if num_a == 0: # num_a es el divisor
                    if num_b == 0:
                        # ¡Aquí es donde la magia ocurre! Invocamos la Onda de Singularidad.
                        print("Detectada singularidad 0/0. Define tu Quantum (ej. Quant (1 = 3, 4 = 6, 7 = 3)):")
                        quant_input = input("> ")
                        # Parseamos los quantums del usuario
                        user_quantums = ZDZ().parse_quantums(quant_input)
                        # Creamos un ZDZ con los quantums del usuario
                        zd_processor = ZDZ(user_quantums)
                        # Generamos la onda desde el punto inicial 1
                        zd_processor.process_wave(1)
                        continue
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
            print(f"Ha ocurrido un error inesperado en la entrada o procesamiento: {e}")

# Iniciar la calculadora
calculadora_zeroniana()