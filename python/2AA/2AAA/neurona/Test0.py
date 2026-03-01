import Neuron as Neun
import xor_id as xorid
# Inicialización de 256 neuronas (8 MB es nada, pero 256 es ultra-veloz)
num_neuronas = 256
memoria_bhl = [Neun.Numeraso2(0, 0, 0) for _ in range(num_neuronas)]
experiencias = [[0, 0, 0] for _ in range(num_neuronas)]

def procesar_texto_en_enjambre(texto):
    # Procesamos de 8 en 8 bytes para generar los IDs
    for i in range(0, len(texto), 8):
        fragmento = texto[i:i+8]
        # Calculamos el ID usando tu lógica de XOR y desplazar
        id_fragmento = xorid.calcular_id_simple(fragmento) 
        
        # Direccionamiento: usamos los bits del ID para elegir neurona
        indice_n = id_fragmento % num_neuronas 
        
        # Extraemos estado actual
        n_gen = memoria_bhl[indice_n]
        exps = experiencias[indice_n]
        
        # Ejecutamos tu lógica branchless de actualización
        n_gen_new, ex0, ex1, ex2 = Neun.Numeraso2_update(exps[0], exps[1], exps[2], n_gen)
        
        # Guardamos el aprendizaje
        memoria_bhl[indice_n] = n_gen_new
        experiencias[indice_n] = [ex0, ex1, ex2]
