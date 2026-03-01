#import requests
#pedir_api_key = input("Ingrese su clave de Gemini: ")

def Inventario(peso):
    posX = 1000
    posY = 1
    espacio = 900*posY
    final = 1
    espacio_ejecución = (final*posX)
    espacio_control = ()%2
    not(espacio_control) and print("El inventario se ha llenado")
    espacio += not(espacio_control)*espacio
    Inventory = espacio + espacio_ejecución + peso
    return Inventory
peso = 0
Inve = Inventario(peso)

print(Inve)
peso = input("¿desea agregar peso?")

