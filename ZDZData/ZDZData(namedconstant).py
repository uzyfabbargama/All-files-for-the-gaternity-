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

# --- Clase Quantum: Representa un Quantum nombrado con sus reglas (N=M) ---
class Quantum:
    _all_quantums = {} # Almacena todos los quantums nombrados globalmente

    def __init__(self, name, rules):
        self.name = name
        self.rules = rules # [(N, M), (N, M), ...]
        Quantum._all_quantums[name] = self # Registramos la instancia en el diccionario global

    def __repr__(self):
        rules_str = ", ".join([f"{n}={m}" for n, m in self.rules])
        return f"Quantum('{self.name}', [{rules_str}])"

    def get_additive_value(self):
        return sum(m for n, m in self.rules)

    # --- Operaciones Mágicas para Quantum + Real ---
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.get_additive_value() + other
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other) 

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return self.get_additive_value() - other
        return NotImplemented
    
    def __rsub__(self, other): 
        if isinstance(other, (int, float)):
            return other - self.get_additive_value()
        return NotImplemented

    def __mul__(self, other): # Quantum * Real (Escala el Quantum)
        if isinstance(other, (int, float)):
            # Modifica self.rules directamente
            self.rules = [(n * other, m * other) for n, m in self.rules]
            return self # Devuelve el mismo objeto Quantum modificado
        return NotImplemented

    def __rmul__(self, other): # Real * Quantum (conmutativa)
        return self.__mul__(other)

    def __truediv__(self, other): # Quantum / Real (Invierte y Multiplica)
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("No se puede dividir un Quantum por cero en esta operación.")
            # Modifica self.rules directamente
            self.rules = [(m * other, n * other) for n, m in self.rules] # Invertir (M,N) y multiplicar por other
            return self # Devuelve el mismo objeto Quantum modificado
        return NotImplemented

    # __rtruediv__ no cambia porque no esperamos 'Real / Quantum' que modifique el Quantum.

    def __floordiv__(self, other): # Usaremos // para la hiperdivisión Q \ A (N/A=M/A)
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("No se puede hiperdividir un Quantum por cero.")
            # Modifica self.rules directamente
            self.rules = [(n / other, m / other) for n, m in self.rules] # N/A=M/A
            return self # Devuelve el mismo objeto Quantum modificado
        return NotImplemented
    
    def __pow__(self, other): # Quantum ** Real (Invierte y Divide)
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("No se puede hipermultiplicar un Quantum por cero.")
            # Modifica self.rules directamente
            self.rules = [(m / other, n / other) for n, m in self.rules] # Invertir (M,N) y dividir por other
            return self # Devuelve el mismo objeto Quantum modificado
        return NotImplemented


# --- Clase para el ZDZ (el "procesador" de la singularidad 0/0) ---
class ZDZ:
    def parse_quantums(self, quant_string):
        quant_list = []
        matches = re.findall(r'(\d+)\s*=\s*(\d+)', quant_string)
        for n_str, m_str in matches:
            quant_list.append((float(n_str), float(m_str))) # Convertir a float para generalidad
        return quant_list

    def transform_point(self, x_in, quant_rules):
        """
        Transforma un punto X usando las reglas de los quantums (como en la onda inicial).
        quant_rules: Lista de tuplas (N, M)
        """
        y_in = float(x_in) 
        x_out = float(x_in)
        y_out = float(y_in)

        # 1. Prioridad por Múltiplos
        found_rule = False
        for n_rule, m_rule in quant_rules:
            if n_rule == 0: continue # Evitar división por cero si N es 0 en una regla

            # Si x_in es un múltiplo de n_rule
            if x_in % n_rule == 0:
                f = x_in / n_rule
                x_out = m_rule * f # X se transforma según la proporción M/N
                y_out = y_in * (m_rule / n_rule) # Y también se escala con la misma proporción
                found_rule = True
                break
        
        # 2. Si no es múltiplo, aplicar la regla de la menor distancia
        if not found_rule and quant_rules: # Asegurarse de que haya reglas para comparar
            distances = {n: abs(x_in - n) for n, m in quant_rules}
            closest_n = min(distances, key=distances.get)
            
            n_rule, m_rule = next((r for r in quant_rules if r[0] == closest_n), (0,0)) # Obtener la regla
            
            if n_rule != 0:
                proportion = m_rule / n_rule
                x_out = x_in * proportion
                y_out = y_in * proportion
            else: # Fallback si la regla más cercana tiene N=0
                x_out = x_in
                y_out = y_in

        # Fallback general si no hay reglas o no se encontró ninguna aplicable
        if not quant_rules:
             x_out = x_in # Por defecto, si no hay reglas, el punto se mantiene
             y_out = x_in # Asumimos Y=X

        return (x_out, y_out)

    def process_wave(self, initial_point_value, quant_rules, num_steps=10):
        """
        Simula la propagación de la "Onda de Singularidad" desde un punto inicial.
        """
        print(f"\n--- Generando Onda de Singularidad ZDZ desde el punto {initial_point_value} ---")
        wave_points = []
        for i in range(1, num_steps + 1):
            x_in = float(i)
            x_out, y_out = self.transform_point(x_in, quant_rules)
            wave_points.append(f"(X{x_out:.3f}, Y{y_out:.3f})")
            print(f"Punto {i}: (X{x_in:.3f}, Y{x_in:.3f}) transformado a {wave_points[-1]}")
        print("\n--- Fin de la Onda de Singularidad ---")
        return wave_points


# --- Función principal de la calculadora ---
def calculadora_zeroniana():
    print("¡Bienvenido a la Calculadora Zeroniana!")
    print("Ingresa tus operaciones. Escribe 'salir' para terminar.")
    print("Puedes usar números normales (ej. 5, 3.14) o crear números DZ (ej. DZ(7)).")
    print("Operadores soportados: +, -, *, /, // (hiperdivisión), ** (hipermultiplicación)")
    print("Reglas especiales de Zerevolution:")
    print(" - N/0 creará un NDZ (Número Dividido por Cero)")
    print(" - DZ(N) * 0 = N (Restitución)")
    print(" - DZ(N) * 1 = 0 (Anulación)")
    print(" - 0 / 0 te permitirá definir y nombrar un Quantum.")
    print(" - Puedes operar con Quantums nombrados (ej. MiQuantum + 5, MiQuantum * 2).")

    zd_processor_instance = ZDZ() # Instancia del procesador ZDZ

    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == 'salir':
                break

            # Pre-procesamiento para reconocer DZ(N) y nombres de Quantums
            processed_input = re.sub(r'(\d+(\.\d+)?)DZ', r'DZ(\1)', user_input)
            
            # Reemplazar nombres de quantums por su representación de objeto
            for q_name, q_obj in Quantum._all_quantums.items():
                # Solo reemplazar si es un nombre de Quantum completo, no un substring
                # Esto es para evitar problemas como reemplazar 'ji' en 'ajito'
                processed_input = re.sub(r'\b' + re.escape(q_name) + r'\b', f"Quantum._all_quantums['{q_name}']", processed_input)
            
            # --- Lógica para manejar 0 / 0 como caso especial ---
            if processed_input.strip() == "0 / 0":
                print("Detectada singularidad 0/0. Define tu Quantum (ej. Quant (1 = 3, 4 = 6)):")
                quant_str_input = input("> ")
                quant_rules_parsed = zd_processor_instance.parse_quantums(quant_str_input)
                
                if not quant_rules_parsed:
                    print("No se pudieron parsear las reglas del Quantum. Inténtalo de nuevo.")
                    continue

                quant_name = input("Asígnale un nombre a este Quantum: ")
                if not quant_name:
                    print("El Quantum necesita un nombre. Inténtalo de nuevo.")
                    continue
                
                # Crear y almacenar el nuevo Quantum
                new_quantum_instance = Quantum(quant_name, quant_rules_parsed)
                print(f"Quantum '{new_quantum_instance.name}' creado: {new_quantum_instance}")
                
                # Opcional: Generar una onda inicial con este Quantum
                print("Generando una onda de prueba con tu nuevo Quantum...")
                zd_processor_instance.process_wave(1, new_quantum_instance.rules)
                continue

            # Para todas las demás operaciones, intentamos evaluarlas.
            try:
                result = eval(processed_input, {'DZ': DZ, 'Quantum': Quantum})
                print(f"Resultado: {result}")
            except ZeroDivisionError as e:
                print(f"Error: {e}")
            except NameError as e:
                print(f"Error: Nombre no definido (ej. {e}). Asegúrate de usar números válidos, el formato DZ(valor) o un Quantum previamente nombrado.")
            except TypeError as e:
                print(f"Error de tipo: {e}. Asegúrate de que las operaciones sean entre tipos compatibles (ej. Quantum + número, DZ * número).")
            except Exception as e:
                print(f"Ha ocurrido un error inesperado al evaluar la expresión: {e}")

        except Exception as e:
            print(f"Ha ocurrido un error inesperado en la entrada o procesamiento general: {e}")

# Iniciar la calculadora
calculadora_zeroniana()