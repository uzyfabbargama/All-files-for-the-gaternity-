import ctypes
import struct

class NeuralScript:
    def __init__(self):
        self.motor = ctypes.CDLL('./libNSMotor.so')
        self.motor.NSMotor.argtypes = [ctypes.c_char_p]
        
    def ejecutar(self, bytecode):
        self.motor.NSMotor(bytecode)

# Crear bytecode
bytecode = b"var \x01\x00\x00\x00\x12\x34\x56\x78\x9a\xbc\xde"
bytecode += b"proc\x01\x00\x00\x00\x02"
bytecode += b"decay \x01\x00\x00\x00\x0a"

# Ejecutar
ns = NeuralScript()
ns.ejecutar(bytecode)
