#importar a script_a como un módulo
import script_a
#accede a valores y funciones exportadas
print(f'Valor de mi variable: {script_a.mi_variable}')
print(f'Valor de mi lista: {script_a.mi_lista}')
print(f'Valor del diccionario: {script_a.mi_diccionario}')

#llama a la función exportada
mensaje = script_a.saludar('Ana')
print(mensaje)