import unittest
import bhl_amp as bhl  # Ahora con el nombre limpio

class StressTestBHL(unittest.TestCase):

    def setUp(self):
        # Valores iniciales (los 1234 que definiste)
        self.base_val = 1234
        self.expB, self.expH, self.expL = 0, 0, 0
        self.numero = bhl.Numeraso(self.base_val, self.base_val, self.base_val)

    def test_detectar_tupla_en_iteraciones_largas(self):
        print("\nIniciando Stress Test para cazar la tupla fantasma...")
        
        # Ejecutamos 50 vueltas de la lógica de actualización
        for i in range(50):
            try:
                # Simulamos lo que pasa dentro del while True de tu script
                # 1. La actualización de Numeraso
                res = bhl.Numeraso_update(self.expB, self.expH, self.expL, self.numero)
                
                # Verificamos si el retorno es una tupla inesperada
                # Numeraso_update devuelve (Numero, expB, expH, expL, tiempo)
                self.assertIsInstance(res, tuple, f"Error en vuelta {i}: La función no devolvió la tupla de control")
                
                # Desempaquetamos
                self.numero, self.expB, self.expH, self.expL, tiempo = res
                
                # EL CHEQUEO CRÍTICO:
                # Verificamos que 'self.numero' no se haya convertido en (valor,)
                self.assertIsInstance(self.numero, (int, float), 
                    f"\n¡CAZADO! En la iteración {i}, la variable 'Numero' se convirtió en tupla: {self.numero}")
                
                # Simulamos la parte de la API (solo los cálculos matemáticos)
                # Aquí es donde sospecho que puede estar el problema:
                # Numero += eval_data.get('ab', 0) * PosX + expB - Necesidad_Social
                
                # Simulamos un incremento típico
                self.numero += 10 * bhl.PosX + self.expB - 100
                
            except Exception as e:
                self.fail(f"El script explotó en la iteración {i} con el error: {e}")

        print(f"Terminadas 50 iteraciones sin errores de tipo. El 'Deep Error' no está aquí.")

if __name__ == '__main__':
    unittest.main()
