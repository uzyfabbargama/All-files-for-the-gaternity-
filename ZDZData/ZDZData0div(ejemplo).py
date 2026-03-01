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

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, DZ):
            return self.value - other.value
        elif isinstance(other, (int, float)):
            return self.value - other
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return other - self.value
        return NotImplemented
    
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
    def __init__(self):
        # Definimos los quantums como reglas internas.
        # Almacenamos en un diccionario para fácil búsqueda.
        # La clave es la coordenada X, el valor es una tupla (Y, X_pareja, Y_pareja)
        self.quantums = {
            1: (6, 6, 1), # (X1, Y6) = (X6, Y1)
            2: (5, 5, 2), # (X2, Y5) = (X5, Y2)
            3: (4, 4, 3), # (X3, Y4) = (X4, Y3)
            4: (3, 3, 4), # (X4, Y3) = (X3, Y4)
            5: (2, 2, 5), # (X5, Y2) = (X2, Y5)
            6: (1, 1, 6)  # (X6, Y1) = (X1, Y6)
        }
    
    def __repr__(self):
        return "ZDZ_Activo (Onda de Singularidad)"

    def process_wave(self, initial_point_value, num_steps=10):
        """
        Simula la propagación de la "Onda de Singularidad" desde un punto inicial.
        initial_point_value: El valor N para el punto inicial (N, N).
        num_steps: Cuántos puntos de la onda generar.
        """
        print(f"\n--- Generando Onda de Singularidad ZDZ desde el punto {initial_point_value} ---")
        wave_points = []
        current_x = initial_point_value
        current_y = initial_point_value

        for i in range(1, num_steps + 1):
            x_in = i # Usamos 'i' como el valor del punto actual para la onda
            y_in = i 

            # Intentar encontrar la regla de transformación en los quantums definidos
            x_out = current_x # Valor por defecto si no hay regla directa
            y_out = current_y # Valor por defecto

            # Lógica para X: buscar en la clave del quantum
            if x_in in self.quantums:
                # Si x_in es una clave (ej. X1), su pareja X_out es el tercer elemento de la tupla
                x_out = self.quantums[x_in][1] 
                
                # Lógica para Y: aplicar la proporción inversa
                y_partner_in_quant = self.quantums[x_in][0] # El Y asociado con X_in en la regla (ej. Y6 para X1)
                
                if y_partner_in_quant != 0: # Evitar división por cero en la proporción
                    proportion = y_in / y_partner_in_quant
                    if proportion < 1: # Si la proporción es menor a 1, resta (tu regla 1 - 1/6)
                        y_out = y_in - proportion 
                    else: # Si la proporción es mayor o igual a 1, suma (tu regla 4 + 4/3)
                        y_out = y_in + proportion
                else:
                    # Caso especial si Y en el quantum es 0 (ej. X7, Y0)
                    y_out = y_in # Mantener Y si la proporción no se puede calcular

            else:
                # Lógica de Extrapolación para X y Y (para números fuera de 1-6)
                # Aquí implementamos tu lógica de "múltiplo común" y "similitud de patrón"
                # Buscamos el quantum más cercano o una relación de escala
                found_rule = False
                for q_x_in, q_vals in self.quantums.items():
                    q_y_in = q_vals[0]
                    q_x_out = q_vals[1]
                    q_y_out = q_vals[2]

                    # Intentamos encontrar un factor 'f' si el punto actual es un múltiplo
                    # Ej. para 8, buscar 4 (f=2)
                    if x_in % q_x_in == 0 and q_x_in != 0:
                        f = x_in / q_x_in
                        # Aplicar la misma proporción X_out/X_in
                        x_out = q_x_out * f # Esto podría ser (X_partner * f)
                        
                        # Aplicar la proporción Y_out/Y_in
                        if q_y_out != 0:
                            y_out = y_in + (q_y_in / q_y_out) * f # Tu regla '8 + 8/6 = Y9.333'
                        else:
                            y_out = y_in

                        found_rule = True
                        break # Encontramos una regla de escalado, salimos del bucle

                if not found_rule:
                    # Si no se encuentra un múltiplo, aplicamos una regla de "suavizado" o "continuación"
                    # Esto es para que la onda no se detenga bruscamente
                    # Podríamos usar la "simetría del 7" como fallback generalizada
                    # Es decir, X_out = Y_in y Y_out = 7 - X_in, o alguna otra tendencia
                    # Por ahora, para simplificar y dejar que tus reglas dominen:
                    # Si no hay regla directa ni escalada, asumimos que X se mantiene y Y intenta acercarse a 7.
                    x_out = x_in 
                    y_out = 7 - x_in # Intenta forzar la simetría del 7 para puntos no cubiertos

            # Actualizar current_x, current_y para el próximo paso (la onda se propaga)
            # Para tu onda de singularidad, cada paso es una "aplicación" de la ZDZ Quant al nuevo 'i'
            # NO se arrastra el resultado anterior, sino que se calcula para cada 'i' de 1 a 10
            # Si quisieras que el resultado de un paso afecte el siguiente,
            # sería: current_x = x_out; current_y = y_out; y usar current_x, current_y como x_in, y_in
            # Pero por tu descripción, cada punto (1..10) se evalúa contra el ZDZ Quant.
            
            wave_points.append(f"(X{x_out:.3f}, Y{y_out:.3f})")
            print(f"Punto {i}: (X{i}, Y{i}) transformado a {wave_points[-1]}")
            
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

    zd_processor = ZDZ() # Creamos una instancia de tu procesador ZDZ

    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == 'salir':
                break

            # Pre-procesamiento: Reemplaza 'NDZ' compactos por 'DZ(N)' para que eval() los reconozca
            # Regex para números enteros o flotantes seguidos de 'DZ'
            processed_input = re.sub(r'(\d+(\.\d+)?)DZ', r'DZ(\1)', user_input)
            
            # Separar la expresión en partes para identificar los operandos y el operador
            parts = processed_input.split()
            
            if len(parts) != 3:
                print("Formato incorrecto. Usa 'operando1 operador operando2' (ej. 5 + 3, DZ(10) * 2).")
                continue

            # Convertir las partes a números o objetos DZ
            try:
                num_b_str, operador, num_a_str = parts
                # Usamos eval() para manejar la creación de objetos DZ si el usuario los escribe como DZ(N)
                # El dict {'DZ': DZ} le dice a eval que 'DZ' se refiere a tu clase DZ
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
                        # Podemos pedir al usuario el punto inicial, o usar uno por defecto (ej. 1)
                        print("Detectada singularidad 0/0. Generando Onda de Singularidad ZDZ...")
                        
                        # Podemos tomar el valor de un operando si es un DZ, o pedir un valor de inicio
                        # Para simplificar, iniciamos la onda desde el '1' como tu ejemplo del 1 al 10.
                        # O podrías pedir: input("Desde qué punto inicial quieres generar la onda (ej. 1): ")
                        initial_wave_point = 1 # O alguna lógica para derivarlo de num_b si no es 0
                        
                        zd_processor.process_wave(initial_wave_point)
                        # No hay un "resultado" único, sino una secuencia de transformaciones
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