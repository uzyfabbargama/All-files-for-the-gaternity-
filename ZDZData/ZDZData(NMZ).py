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
                return 0 # Anulación
            else:
                return DZ(self.value * other) 
        elif isinstance(other, DZ):
            return DZ(self.value * other.value)
        elif isinstance(other, NMZ): # NMZ * DZ
            # NMZ * DZ = (Valor NMZ * Valor DZ) ?
            # Por ahora, para simplificar, no definiremos NMZ * DZ explícitamente aquí.
            return NotImplemented
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
                # Esto es N / 0, que ya genera un NDZ. No creo un nuevo NDZ aquí,
                # asumo que el N/0 inicial ya lo manejó.
                # Si DZ / 0, podría ser un ZDZ si DZ representa un 0.
                return NotImplemented # O podrías definir DZ(self.value) / 0 = ZDZ() si self.value es 0
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

# --- Clase NMZ: Nuevo Número Multiplicado por Cero ---
class NMZ:
    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("El valor de un número NMZ debe ser numérico.")
        self.value = value

    def __repr__(self):
        return f"NMZ({self.value})"

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                # AHORA CORRECTO: NMZ / 0 = N (valor original del NMZ)
                return self.value 
            elif other == 1:
                return 0
            else:
                return NMZ(self.value / other)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                # AHORA CORRECTO: NMZ * 0 = ZDZ
                return ZDZ_Default() 
            elif other == 1:
                return 0
            else:
                return NMZ(self.value * other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)
    
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

    # --- Operaciones Mágicas para Quantum + Real (modifican el Quantum in-place si es multiplicativa/divisiva) ---
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
            self.rules = [(n * other, m * other) for n, m in self.rules]
            return self # Devuelve el mismo objeto Quantum modificado
        return NotImplemented

    def __rmul__(self, other): # Real * Quantum (conmutativa)
        return self.__mul__(other)

    def __truediv__(self, other): # Quantum / Real (Invierte y Multiplica)
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("No se puede dividir un Quantum por cero en esta operación.")
            self.rules = [(m * other, n * other) for n, m in self.rules] # Invertir (M,N) y multiplicar por other
            return self # Devuelve el mismo objeto Quantum modificado
        return NotImplemented

    def __floordiv__(self, other): # Usaremos // para la hiperdivisión Q \ A (N/A=M/A)
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("No se puede hiperdividir un Quantum por cero.")
            self.rules = [(n / other, m / other) for n, m in self.rules] # N/A=M/A
            return self # Devuelve el mismo objeto Quantum modificado
        return NotImplemented
    
    def __pow__(self, other): # Quantum ** Real (Invierte y Divide)
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("No se puede hipermultiplicar un Quantum por cero.")
            self.rules = [(m / other, n / other) for n, m in self.rules] # Invertir (M,N) y dividir por other
            return self # Devuelve el mismo objeto Quantum modificado
        return NotImplemented

# --- Clase ZDZ_Default: Representa el 0/0 con comportamiento predeterminado sin Quantum ---
class ZDZ_Default:
    def __repr__(self):
        return "ZDZ" # Representación textual de la singularidad por defecto

    # Implementa las reglas N + ZDZ = NDZ, N * ZDZ = NMZ, etc.
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return DZ(other) # N + ZDZ = NDZ
        return NotImplemented

    def __radd__(self, other): # other + ZDZ
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            # N * ZDZ = NMZ
            # Basado en tu lógica de inversion y NMZ = N*1*0*1
            # Si ZDZ invierte 0 y 1, entonces N * ZDZ es N * (0_inv / 0_inv)
            # Que llevaría a NMZ(N)
            return NMZ(other) # N * ZDZ = NMZ(N)
        return NotImplemented

    def __rmul__(self, other): # other * ZDZ
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                # ZDZ / 0, esto es una doble singularidad, podria ser indefinido o un ZDZ especial.
                # Por ahora, simplemente devolveremos ZDZ
                return ZDZ_Default()
            # N / ZDZ = NDZ normal
            # Basado en tu regla N/1 / 0/0 = NDZ normal
            # Cuando ZDZ está en el denominador, "transforma" el numerador en un NDZ.
            return DZ(other) # other / ZDZ = DZ(other)
        return NotImplemented

    def __rtruediv__(self, other): # other / ZDZ
        return self.__truediv__(other) # Asumimos misma lógica

# --- Clase para el ZDZ (el "procesador" de la singularidad 0/0 y la onda) ---
class ZDZProcessor: # Renombré para evitar conflicto con ZDZ_Default
    def parse_quantums(self, quant_string):
        quant_list = []
        matches = re.findall(r'(\d+(\.\d+)?)\s*=\s*(\d+(\.\d+)?)', quant_string)
        for n_str, m_str in matches:
            quant_list.append((float(n_str), float(m_str)))
        return quant_list

    def transform_point(self, x_in, quant_rules):
        # (La lógica de transform_point es la misma que antes)
        y_in = float(x_in) 
        x_out = float(x_in)
        y_out = float(y_in)

        found_rule = False
        for n_rule, m_rule in quant_rules:
            if n_rule == 0: continue
            if x_in % n_rule == 0:
                f = x_in / n_rule
                x_out = m_rule * f
                y_out = y_in * (m_rule / n_rule)
                found_rule = True
                break
        
        if not found_rule and quant_rules:
            distances = {n: abs(x_in - n) for n, m in quant_rules}
            closest_n = min(distances, key=distances.get)
            
            n_rule, m_rule = next((r for r in quant_rules if r[0] == closest_n), (0,0))
            
            if n_rule != 0:
                proportion = m_rule / n_rule
                x_out = x_in * proportion
                y_out = y_in * proportion
            else:
                x_out = x_in
                y_out = y_in

        if not quant_rules:
             x_out = x_in
             y_out = x_in

        return (x_out, y_out)

    def process_wave(self, initial_point_value, quant_rules, num_steps=10):
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
    print(" - 0 / 0 te permitirá definir y nombrar un Quantum, o interactuar con ZDZ por defecto.")
    print(" - Puedes operar con Quantums nombrados (ej. MiQuantum + 5, MiQuantum * 2).")
    print(" - Nuevos números: NMZ (Número Multiplicado por Cero), y ZDZ (la Singularidad misma).")


    zd_processor_instance = ZDZProcessor() # Instancia del procesador ZDZ

    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == 'salir':
                break

            processed_input = user_input
            # Reemplazar N/0 con DZ(N) antes de eval para que Python no lance ZeroDivisionError
            # Esto debe ser inteligente para no reemplazar el 0/0 que queremos manejar aparte.
            # Regex para N / 0 (N != 0)
            processed_input = re.sub(r'(\b\d+(\.\d+)?)\s*\/\s*0\b(?!(\s*\/\s*0))', r'DZ(\1)', processed_input)

            # Reemplazar '0 / 0' con la instancia ZDZ_Default si no es para definir un Quantum
            # Lo hacemos aquí para que eval() lo interprete directamente si no se entra al modo Quantum
            is_quantum_definition = False
            if user_input.strip() == "0 / 0":
                print("Detectada singularidad 0/0.")
                response = input("¿Deseas definir un Quantum ahora? (s/n): ").lower()
                if response == 's':
                    is_quantum_definition = True
                else:
                    # Si no se define Quantum, 0/0 se convierte en ZDZ_Default para operaciones
                    processed_input = "ZDZ_Default()" 
            
            # Si estamos en modo definición de Quantum
            if is_quantum_definition:
                print("Define tu Quantum (ej. Quant (1 = 3, 4 = 6)):")
                quant_str_input = input("> ")
                quant_rules_parsed = zd_processor_instance.parse_quantums(quant_str_input)
                
                if not quant_rules_parsed:
                    print("No se pudieron parsear las reglas del Quantum. Inténtalo de nuevo.")
                    continue

                quant_name = input("Asígnale un nombre a este Quantum: ")
                if not quant_name:
                    print("El Quantum necesita un nombre. Inténtalo de nuevo.")
                    continue
                
                new_quantum_instance = Quantum(quant_name, quant_rules_parsed)
                print(f"Quantum '{new_quantum_instance.name}' creado: {new_quantum_instance}")
                
                print("Generando una onda de prueba con tu nuevo Quantum...")
                zd_processor_instance.process_wave(1, new_quantum_instance.rules)
                continue

            # Reemplazar nombres de quantums por su representación de objeto
            for q_name, q_obj in Quantum._all_quantums.items():
                processed_input = re.sub(r'\b' + re.escape(q_name) + r'\b', f"Quantum._all_quantums['{q_name}']", processed_input)
            
            # Incluir NMZ y ZDZ_Default en el contexto de eval
            context = {'DZ': DZ, 'Quantum': Quantum, 'NMZ': NMZ, 'ZDZ_Default': ZDZ_Default}

            try:
                result = eval(processed_input, context)
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