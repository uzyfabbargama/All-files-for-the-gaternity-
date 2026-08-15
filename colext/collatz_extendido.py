def decimal_parity_sequence(x, max_steps=1000, filename="collatz_states.txt"):
    """
    Aplica las reglas extendidas de Collatz basadas en la paridad de los dígitos decimales.
    
    Reglas:
    - Si el número es entero (sin parte decimal): aplica Collatz clásico
    - Si tiene parte decimal:
        * r = (1 si parte entera es impar else 0) + (número de dígitos decimales impares)
        * Si r > 0: x -> 3^r * x + (0.111... con r unos)
        * Si r = 0: x -> x/2
    
    Args:
        x: número inicial (float)
        max_steps: máximo de iteraciones (por si no converge)
        filename: nombre del archivo de salida
    """
    
    def get_digits_parity(n):
        """Obtiene los dígitos decimales de n y cuenta cuántos son impares"""
        # Convertir a string para analizar dígitos
        str_n = f"{n:.15f}".rstrip('0').rstrip('.')
        
        if '.' not in str_n:
            return [], 0  # Sin decimales
        
        decimal_part = str_n.split('.')[1]
        # Limitar a primeros 15 dígitos para no explotar
        decimal_part = decimal_part[:15]
        
        digits = [int(d) for d in decimal_part]
        odd_count = sum(1 for d in digits if d % 2 == 1)
        
        return digits, odd_count
    
    def next_state(x):
        """Calcula el siguiente estado según las reglas"""
        # Verificar si es entero (cerca de un entero)
        epsilon = 1e-10
        if abs(x - round(x)) < epsilon:
            # Collatz clásico para enteros
            n = int(round(x))
            if n % 2 == 0:
                return n // 2
            else:
                return 3 * n + 1
        
        # Para números no enteros
        # Obtener parte entera y decimal
        integer_part = int(x)
        
        # Obtener dígitos decimales y contar impares
        try:
            # Formatear para evitar notación científica
            str_x = f"{x:.15f}"
            if 'e' in str_x:
                str_x = f"{x:.15f}"
            
            if '.' in str_x:
                decimal_str = str_x.split('.')[1].rstrip('0')
                if not decimal_str:  # Si después de quitar ceros no hay decimales
                    digits_odd = 0
                else:
                    # Tomar primeros dígitos significativos
                    decimal_digits = [int(d) for d in decimal_str[:15]]
                    digits_odd = sum(1 for d in decimal_digits if d % 2 == 1)
            else:
                digits_odd = 0
        except:
            # Fallback: método alternativo
            decimal_part = x - integer_part
            if decimal_part < 1e-10:
                digits_odd = 0
            else:
                # Convertir a string de forma segura
                decimal_str = f"{decimal_part:.15f}".split('.')[1].rstrip('0')
                if not decimal_str:
                    digits_odd = 0
                else:
                    decimal_digits = [int(d) for d in decimal_str[:15]]
                    digits_odd = sum(1 for d in decimal_digits if d % 2 == 1)
        
        # Calcular r
        r = (1 if integer_part % 2 == 1 else 0) + digits_odd
        
        if r == 0:
            # Todos pares: dividir por 2
            return x / 2
        else:
            # Aplicar multiplicación por 3^r y suma de 1...1 con r unos
            multiplier = 3 ** r
            # Construir el sumando: 0.111... con r unos
            sumand = sum(10**(-i) for i in range(1, r+1))
            # El sumando debe ser exactamente 0.111... con r dígitos
            # Pero para evitar errores de redondeo, usamos fracción
            sumand = float(f"0.{'1'*r}")
            
            return multiplier * x + sumand
    
    # Abrir archivo para escritura
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Secuencia de Collatz extendido para x0 = {x}\n")
        f.write("="*60 + "\n\n")
        
        current = x
        visited = {}  # Para detectar ciclos
        step = 0
        
        while step < max_steps:
            # Guardar estado actual
            f.write(f"Paso {step:4d}: {current:.10f}\n")
            print(f"Paso {step:4d}: {current:.10f}")
            
            # Detectar ciclo
            key = round(current, 10)  # Redondear para comparación
            if key in visited:
                f.write(f"\n¡CICLO DETECTADO! El paso {visited[key]} se repite en paso {step}\n")
                print(f"\n¡CICLO DETECTADO! El paso {visited[key]} se repite en paso {step}")
                break
            
            visited[key] = step
            
            # Calcular siguiente estado
            next_val = next_state(current)
            
            # Verificar convergencia a 1 (pero solo para enteros)
            if abs(next_val - 1) < 1e-8 and abs(next_val - round(next_val)) < 1e-8:
                f.write(f"Paso {step+1:4d}: {next_val:.10f}\n")
                f.write(f"\n¡CONVERGE A 1! en paso {step+1}\n")
                print(f"Paso {step+1:4d}: {next_val:.10f}")
                print(f"\n¡CONVERGE A 1! en paso {step+1}")
                break
            
            current = next_val
            step += 1
        
        if step >= max_steps:
            f.write(f"\nLímite de {max_steps} pasos alcanzado\n")
            print(f"\nLímite de {max_steps} pasos alcanzado")
        
        f.write(f"\nTotal de pasos: {step+1}\n")
    
    print(f"\nResultados guardados en '{filename}'")

# Ejecutar para 0.27
if __name__ == "__main__":
    # Puedes cambiar el número aquí
    numero_inicial = 0.27
    decimal_parity_sequence(numero_inicial, max_steps=500, filename="collatz_0.27.txt")
