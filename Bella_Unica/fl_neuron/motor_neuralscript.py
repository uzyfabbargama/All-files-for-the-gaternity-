#!/usr/bin/env python3
# motor_neuralscript.py - ¡AHORA CON DECIMALES!

import ctypes
from preprocesador_v4 import parse_and_serialize

class MotorNeuralScript:
    def __init__(self):
        self.lib = ctypes.CDLL('./libNSMotor.so')
        self.lib.NSMotor.argtypes = [ctypes.c_char_p]
        self.lib.NSMotor.restype = None
        
    def ejecutar(self, codigo_fuente):
        """Compila y ejecuta código NeuralScript"""
        bytecode, neuron_map, logic_map, func_map = parse_and_serialize(codigo_fuente)
        self.lib.NSMotor(bytes(bytecode))
        return neuron_map, logic_map, func_map

if __name__ == "__main__":
    motor = MotorNeuralScript()
    
    print("🧠 MOTOR NEURALSCRIPT V3 - EJECUCIÓN DIRECTA")
    print("="*60)
    
    # EJEMPLO 1: Red simple con decimales
    print("\n📝 EJEMPLO 1: Red neuronal con decimales")
    codigo1 = """
    $ Red de 2 neuronas
    var entrada1, 0.1
    var entrada2, 0.2
    proc entrada1, entrada2
    """
    motor.ejecutar(codigo1)
    print("✅ Red con decimales ejecutada")
    
    # EJEMPLO 2: Red de 3 capas con decimales
    print("\n📝 EJEMPLO 2: Red de 3 capas con decimales")
    codigo2 = """
    $ Capa de entrada
    var entrada1, 0.1
    var entrada2, 0.2
    
    $ Capa oculta
    var capa1, 0.3
    var capa2, 0.4
    
    $ Capa de salida
    var salida, 0.5
    
    $ Procesar
    proc capa1, entrada1
    proc capa2, entrada2
    proc salida, capa1
    proc salida, capa2
    """
    motor.ejecutar(codigo2)
    print("✅ Red de 3 capas con decimales ejecutada")
    
    print("\n" + "="*60)
    print("🎉 ¡TODOS LOS EJEMPLOS EJECUTADOS CORRECTAMENTE!")
    print("🚀 Motor NeuralScript con soporte completo para decimales")
