import time
import math
import uuid
import json
import os
class MemoriaSocial:
    """
    Clase que implementa la base de datos de memoria social para la IA.

    Esta clase maneja la información de hasta 150 usuarios, con un algoritmo
    inteligente para olvidar a los usuarios menos significativos.
    """
    def __init__(self, nombre_ia):
        """
        Inicializa la base de datos de la memoria social.

        Args:
            nombre_ia (str): El nombre de la IA, que se usa para nombrar el archivo de la base de datos.
        """
        self.nombre_ia = nombre_ia
        self.db_name = f"{self.nombre_ia}_memoria_social.json"
        self.limite_maximo = 150  # El número de Dunbar, el límite de relaciones significativas.
        self.db = {}  # Un diccionario para almacenar los perfiles de los usuarios.
        self._cargar_estado()

    def _cargar_estado(self):
        """Carga el estado de la base de datos desde un archivo JSON."""
        try:
            with open(self.db_name, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
            print(f"--- Memoria social cargada desde '{self.db_name}' ---")
        except FileNotFoundError:
            print(f"--- No se encontró el archivo '{self.db_name}'. Creando una nueva memoria social. ---")

    def _guardar_estado(self):
        """Guarda el estado actual de la base de datos en un archivo JSON."""
        with open(self.db_name, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, indent=4)
        print(f"--- Memoria social guardada en '{self.db_name}' ---")

    def agregar_o_actualizar_usuario(self, nombre_usuario, bhl_values, relacion_anterior=None):
        """
        Agrega o actualiza el perfil de un usuario.

        Args:
            nombre_usuario (str): El nombre del usuario.
            bhl_values (dict): Un diccionario con los valores de BHL (Bondad, Hostilidad, Lógica, Ego).
            relacion_anterior (dict): (Opcional) Los datos de la relación previa para actualizar.
        """
        if nombre_usuario in self.db:
            # Si el usuario ya existe, actualiza su perfil
            perfil = self.db[nombre_usuario]
            perfil['variables_BHL'] = bhl_values
            
            # Actualiza el tiempo de la última interacción
            tiempo_interaccion_actual = time.time()
            perfil['variables_tiempo']['ultima_interaccion'] = tiempo_interaccion_actual
            
            # Actualiza el tiempo total de la relación. Si hay una relación anterior, usa esa.
            if relacion_anterior:
                tiempo_desde_ultima = tiempo_interaccion_actual - perfil['variables_tiempo']['ultima_interaccion']
                perfil['variables_tiempo']['tiempo_relacion'] += tiempo_desde_ultima
            else:
                # Si es la primera vez que se interactúa en esta sesión, solo actualiza la última interacción
                perfil['variables_tiempo']['tiempo_relacion'] += 0

            print(f"--- Perfil de '{nombre_usuario}' actualizado. ---")

        else:
            # Si el usuario es nuevo, verifica el límite de 150
            if len(self.db) >= self.limite_maximo:
                self._olvidar_usuario_menos_significativo()

            # Crea el perfil del nuevo usuario
            self.db[nombre_usuario] = {
                'id': str(uuid.uuid4()),
                'variables_BHL': bhl_values,
                'variables_tiempo': {
                    'primera_interaccion': time.time(),
                    'ultima_interaccion': time.time(),
                    'tiempo_relacion': 0
                }
            }
            print(f"--- Nuevo perfil para '{nombre_usuario}' creado. ---")
            
        self._guardar_estado()

    def _olvidar_usuario_menos_significativo(self):
        """
        Implementa el algoritmo central para olvidar a un usuario.

        Encuentra al usuario más "promedio" o "superficial" para eliminarlo.
        Prioriza la eliminación de perfiles que no se destacan en bondad, hostilidad
        o lógica, a pesar del tiempo que haya pasado.
        """
        if not self.db:
            return  # No hay usuarios para olvidar

        # 1. Calcular la media de los valores BHL para todos los usuarios
        total_b = 0
        total_h = 0
        total_l = 0
        count = len(self.db)

        if count > 0:
            for perfil in self.db.values():
                bhl = perfil['variables_BHL']
                total_b += bhl.get('Bondad', 0)
                total_h += bhl.get('Hostilidad', 0)
                total_l += bhl.get('Lógica', 0)

            media_b = total_b / count
            media_h = total_h / count
            media_l = total_l / count
        else:
            return

        usuario_a_olvidar = None
        max_puntuacion_olvido = -1

        # 2. Iterar sobre los perfiles para encontrar al más "superficial"
        for nombre_usuario, perfil in self.db.items():
            bhl = perfil['variables_BHL']
            
            # Calcular la "distancia" del usuario a la media del grupo (un proxy de cuán "promedio" es)
            distancia_media = math.sqrt(
                (bhl.get('Bondad', 0) - media_b)**2 +
                (bhl.get('Hostilidad', 0) - media_h)**2 +
                (bhl.get('Lógica', 0) - media_l)**2
            )

            # Calcular el tiempo de inactividad
            tiempo_inactividad = time.time() - perfil['variables_tiempo']['ultima_interaccion']

            # Calcular el "tiempo de relación"
            tiempo_relacion = perfil['variables_tiempo']['tiempo_relacion']

            # 3. Calcular la puntuación de "olvido".
            # La lógica es: a mayor "superficialidad" (baja distancia), mayor tiempo de inactividad,
            # y menor tiempo de relación, más probable es que se olvide.
            # Los pesos pueden ajustarse, pero la lógica central es que los que se destacan
            # (baja superficialidad) son más importantes de recordar.
            # Se puede usar una fórmula simple como: (superficialidad * inactividad) / (tiempo_relacion + 1)
            puntuacion_olvido = (1 / (distancia_media + 1)) * (tiempo_inactividad / (tiempo_relacion + 1))
            
            # La puntuación más alta indica el candidato ideal para ser olvidado
            if puntuacion_olvido > max_puntuacion_olvido:
                max_puntuacion_olvido = puntuacion_olvido
                usuario_a_olvidar = nombre_usuario
        
        if usuario_a_olvidar:
            print(f"--- Límite de memoria alcanzado. Olvidando a '{usuario_a_olvidar}' por ser el menos significativo. ---")
            del self.db[usuario_a_olvidar]

    def obtener_perfil(self, nombre_usuario):
        """Devuelve el perfil de un usuario si existe."""
        return self.db.get(nombre_usuario, None)

    def mostrar_memoria(self):
        """Muestra todos los perfiles en la base de datos."""
        print("-" * 50)
        print(f"Memoria Social de la IA '{self.nombre_ia}'")
        print("-" * 50)
        for nombre, perfil in self.db.items():
            print(f"Usuario: {nombre}")
            print(f"  ID: {perfil['id']}")
            print(f"  BHL: {perfil['variables_BHL']}")
            print(f"  Tiempo Relación: {round(perfil['variables_tiempo']['tiempo_relacion'], 2)}s")
            print(f"  Última Interacción: {time.ctime(perfil['variables_tiempo']['ultima_interaccion'])}")
            print("-" * 20)
        print(f"Total de usuarios: {len(self.db)}")
        print("-" * 50)
