using UnityEngine;
using System.Collections.Generic;
using System.Linq; // Para usar .ToList()

public class NumeriumChunkGenerator : MonoBehaviour
{
    // --- Parámetros de Configuración del Mundo (ajustables en el Inspector de Unity) ---
    [Header("Configuración del Mundo")]
    public int globalSeed = 12345; // Semilla global para la generación del mundo Numerium
    public int chunkSize = 16;     // Tamaño de cada chunk (ej. 16x16 bloques en X y Z)
    public int renderDistance = 3; // Cuántos chunks alrededor del jugador deben estar cargados
    public int maxYHeight = 32;    // Altura máxima que puede alcanzar el terreno en un chunk
    public int fillDensity = 5;    // Cuántas "veces" se intenta colocar un bloque por cada (x,z) en el chunk (afecta la densidad del terreno)

    [Header("Referencias de Objetos")]
    public GameObject player; // Arrastra tu GameObject de jugador aquí desde la escena
    public GameObject voxelPrefab; // Arrastra un prefab de cubo simple para tus bloques

    // Diccionario para almacenar los chunks cargados y sus GameObjects
    // Key: Vector2Int (coordenadas del chunk), Value: GameObject (padre que contiene los voxeles del chunk)
    private Dictionary<Vector2Int, GameObject> loadedChunks = new Dictionary<Vector2Int, GameObject>();

    // Variables para el seguimiento de la posición del jugador
    private Vector2Int lastPlayerChunkCoords;

    // --- Métodos de Unity Lifecycle ---
    void Start()
    {
        // Asegúrate de que el jugador esté asignado
        if (player == null)
        {
            Debug.LogError("Player GameObject no asignado al generador de chunks.");
            enabled = false; // Deshabilita el script si no hay jugador
            return;
        }

        // Calcula las coordenadas del chunk inicial del jugador
        lastPlayerChunkCoords = GetPlayerChunkCoords();
        
        // Carga los chunks iniciales alrededor del jugador
        UpdateChunksBasedOnPlayerPos(lastPlayerChunkCoords.x, lastPlayerChunkCoords.y);
    }

    void Update()
    {
        // Calcula las coordenadas del chunk actual del jugador en cada frame
        Vector2Int currentPlayerChunkCoords = GetPlayerChunkCoords();

        // Si el jugador se ha movido a un nuevo chunk, actualiza los chunks cargados/descargados
        if (currentPlayerChunkCoords != lastPlayerChunkCoords)
        {
            UpdateChunksBasedOnPlayerPos(currentPlayerChunkCoords.x, currentPlayerChunkCoords.y);
            lastPlayerChunkCoords = currentPlayerChunkCoords;
        }
    }

    // --- Lógica de Numerium ---
    // Función de mapeo para las coordenadas (x, z) dentro de una cuadrícula.
    // Adapta la lógica de Python a C#.
    private Vector2Int MapValueToCoords(int val, int gridX, int gridZ)
    {
        int valMod100 = val % 100;
        int mappedX, mappedZ;

        // Casos específicos para generar los patrones de "árbol" o "pilar"
        // Los valores se definen como en Python
        if (valMod100 == 50 || valMod100 == 51 || valMod100 == 0 || valMod100 == 2 || valMod100 == 4 || 
            valMod100 == 6 || valMod100 == 8 || valMod100 == 53 || valMod100 == 55 || 
            valMod100 == 57 || valMod100 == 59)
        {
            mappedX = 2;
            mappedZ = 2;
        }
        else if (valMod100 == 10)
        {
            mappedX = 1;
            mappedZ = 1;
        }
        else
        {
            // Mapeo por defecto: usamos la decena para X y la unidad para Z
            int tensDigit = (int)Mathf.Floor(valMod100 / 10);
            int unitsDigit = valMod100 % 10;
            mappedX = tensDigit % gridX;
            mappedZ = unitsDigit % gridZ;
        }

        return new Vector2Int(mappedX, mappedZ);
    }

    // Función para generar un chunk de mundo Numerium
    private List<VoxelData> GenerateNumeriumChunk(int seed, int chunkX, int chunkZ)
    {
        // Diccionario para almacenar las alturas acumuladas para cada (x_local, z_local) dentro de este chunk
        Dictionary<Vector2Int, int> chunkHeights = new Dictionary<Vector2Int, int>();

        // El valor inicial de la secuencia de Numerium para este chunk.
        // Los multiplicadores grandes aseguran que chunks vecinos tengan secuencias de números iniciales muy diferentes.
        long currentSequenceValue = seed + (long)chunkX * 1000000000L + (long)chunkZ * 10000L;

        List<VoxelData> voxelsToRender = new List<VoxelData>();

        // Número de iteraciones para "poblar" el chunk (densidad y altura).
        int numFillingIterations = chunkSize * chunkSize * fillDensity;

        for (int i = 0; i < numFillingIterations; i++)
        {
            // Mapeamos el valor actual de la secuencia a coordenadas locales (base 3x3)
            Vector2Int mapped3x3 = MapValueToCoords((int)currentSequenceValue, 3, 3);

            // Ajustamos las coordenadas mapeadas al tamaño real del chunk
            int xInChunk = mapped3x3.x % chunkSize;
            int zInChunk = mapped3x3.y % chunkSize;

            // Obtenemos la altura actual para esta posición local
            int currentY = 0;
            if (chunkHeights.ContainsKey(new Vector2Int(xInChunk, zInChunk)))
            {
                currentY = chunkHeights[new Vector2Int(xInChunk, zInChunk)];
            }

            // Incrementamos la altura, limitando a la altura máxima del chunk
            chunkHeights[new Vector2Int(xInChunk, zInChunk)] = Mathf.Min(currentY + 1, maxYHeight - 1);

            // Avanzamos la secuencia de Numerium sumando la semilla global
            currentSequenceValue += seed;
        }

        // Construimos los datos de los voxeles para renderizar basados en las alturas finales
        for (int x = 0; x < chunkSize; x++)
        {
            for (int z = 0; z < chunkSize; z++)
            {
                int height = 0;
                if (chunkHeights.ContainsKey(new Vector2Int(x, z)))
                {
                    height = chunkHeights[new Vector2Int(x, z)];
                }

                // Para cada nivel hasta la altura generada, añade un bloque
                for (int y = 0; y <= height; y++)
                {
                    // Coordenadas globales del bloque
                    Vector3 globalPos = new Vector3(
                        (float)chunkX * chunkSize + x,
                        (float)y,
                        (float)chunkZ * chunkSize + z
                    );

                    // Asignamos un color simple basado en la altura (ejemplo visual)
                    Color blockColor;
                    if (globalPos.y < maxYHeight * 0.2f)
                    {
                        blockColor = new Color(80f / 255f, 40f / 255f, 20f / 255f); // Tierra oscura
                    }
                    else if (globalPos.y < maxYHeight * 0.5f)
                    {
                        blockColor = Color.green; // Hierba
                    }
                    else
                    {
                        blockColor = Color.gray; // Piedra o nieve
                    }

                    voxelsToRender.Add(new VoxelData(globalPos, blockColor));
                }
            }
        }
        return voxelsToRender;
    }

    // Estructura auxiliar para almacenar los datos de un voxel
    private struct VoxelData
    {
        public Vector3 position;
        public Color color;

        public VoxelData(Vector3 pos, Color col)
        {
            position = pos;
            color = col;
        }
    }

    // --- Métodos de Gestión de Chunks ---
    private Vector2Int GetPlayerChunkCoords()
    {
        // Calcula las coordenadas del chunk en el que se encuentra el jugador
        return new Vector2Int(
            Mathf.FloorToInt(player.transform.position.x / chunkSize),
            Mathf.FloorToInt(player.transform.position.z / chunkSize)
        );
    }

    private void UpdateChunksBasedOnPlayerPos(int playerChunkX, int playerChunkZ)
    {
        HashSet<Vector2Int> chunksToLoadSet = new HashSet<Vector2Int>();
        for (int dx = -renderDistance; dx <= renderDistance; dx++)
        {
            for (int dz = -renderDistance; dz <= renderDistance; dz++)
            {
                chunksToLoadSet.Add(new Vector2Int(playerChunkX + dx, playerChunkZ + dz));
            }
        }

        // Carga chunks nuevos
        foreach (Vector2Int chunkCoords in chunksToLoadSet)
        {
            LoadChunk(chunkCoords.x, chunkCoords.y);
        }

        // Descarga chunks fuera de rango
        List<Vector2Int> chunksToUnload = new List<Vector2Int>();
        foreach (var entry in loadedChunks)
        {
            if (!chunksToLoadSet.Contains(entry.Key))
            {
                chunksToUnload.Add(entry.Key);
            }
        }

        foreach (Vector2Int chunkCoords in chunksToUnload)
        {
            UnloadChunk(chunkCoords.x, chunkCoords.y);
        }
    }

    private void LoadChunk(int cx, int cz)
    {
        Vector2Int chunkCoords = new Vector2Int(cx, cz);
        if (loadedChunks.ContainsKey(chunkCoords))
        {
            return;
        }

        Debug.Log($"Loading chunk: ({cx}, {cz})");

        // Crea un GameObject padre para el chunk para mantener la jerarquía de la escena limpia
        GameObject chunkGameObject = new GameObject($"Chunk_{cx}_{cz}");
        chunkGameObject.transform.parent = this.transform; // Haz que el generador sea el padre de los chunks

        // Genera los datos del chunk Numerium
        List<VoxelData> voxelData = GenerateNumeriumChunk(globalSeed, cx, cz);

        // Crea y añade GameObjects de voxel al chunk
        foreach (VoxelData data in voxelData)
        {
            GameObject voxel = Instantiate(voxelPrefab, data.position, Quaternion.identity);
            voxel.GetComponent<Renderer>().material.color = data.color; // Asigna el color
            voxel.transform.parent = chunkGameObject.transform; // Haz que el voxel sea hijo del chunk GameObject
        }

        loadedChunks.Add(chunkCoords, chunkGameObject);
    }

    private void UnloadChunk(int cx, int intz)
    {
        Vector2Int chunkCoords = new Vector2Int(cx, intz);
        if (loadedChunks.ContainsKey(chunkCoords))
        {
            Debug.Log($"Unloading chunk: ({cx}, {intz})");
            Destroy(loadedChunks[chunkCoords]); // Elimina el GameObject padre del chunk y todos sus hijos
            loadedChunks.Remove(chunkCoords);
        }
    }
}