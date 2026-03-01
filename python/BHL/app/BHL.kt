import com.google.gson.Gson
import com.google.gson.annotations.SerializedName
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.File
import java.io.FileReader
import java.io.FileWriter
import java.io.IOException
import kotlin.math.max
import kotlin.math.min
import kotlin.random.Random

// URL de la API de Gemini
const val GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
const val SAVE_FILE_NAME = "bhl_session_data.json"

val client = OkHttpClient()
val gson = Gson()
val JSON = "application/json; charset=utf-8".toMediaType()

data class ChatMessage(val user: String, val character: String)

@kotlin.jvm.JvmRecord
data class CharacterState(
    @SerializedName("bhl_values") var numero: Double = 50.0,
    @SerializedName("Exp_B") var expB: Double = 0.0,
    @SerializedName("Exp_H") var expH: Double = 0.0,
    @SerializedName("Exp_L") var expL: Double = 0.0,
    @SerializedName("chs_values") var numero1: Double = 50.0,
    @SerializedName("Exp_S") var expS: Double = 0.0,
    @SerializedName("Exp_Hu") var expHu: Double = 0.0,
    @SerializedName("Exp_C") var expC: Double = 0.0,
    @SerializedName("chat_history") val chatHistory: MutableList<ChatMessage> = mutableListOf(),
    var nivelIncomodidad: Double = 0.0,
    var scenario: String = ""
)

fun saveState(state: CharacterState) {
    try {
        FileWriter(SAVE_FILE_NAME).use { writer ->
            gson.toJson(state, writer)
        }
        println("\n--- Estado del personaje guardado en '$SAVE_FILE_NAME' ---")
    } catch (e: IOException) {
        println("Error al guardar el estado: ${e.message}")
    }
}

fun loadState(): CharacterState {
    val file = File(SAVE_FILE_NAME)
    if (!file.exists()) {
        println("\n--- No se encontró el archivo de estado. Creando uno nuevo. ---")
        return CharacterState()
    }

    return try {
        FileReader(file).use { reader ->
            gson.fromJson(reader, CharacterState::class.java).apply {
                println("\n--- Estado del personaje cargado desde '$SAVE_FILE_NAME' ---")
            }
        }
    } catch (e: IOException) {
        println("Error al cargar el estado: ${e.message}")
        CharacterState()
    }
}

fun calculateValues(currentValue: Double, minVal: Double, maxVal: Double, factor: Double): Double {
    return min(max(currentValue + (factor * (Random.nextInt(20, 101) / 100.0)), minVal), maxVal)
}

fun generatePromptForIa(message: String, state: CharacterState): String {
    // Procesar el input del usuario para ajustar los valores del personaje
    val messageLower = message.lowercase()
    if (listOf("amor", "amar", "cariño", "respeto", "amabilidad", "bondad").any { it in messageLower }) {
        state.numero = calculateValues(state.numero, 0.0, 100.0, 10.0)
        state.expB = min(state.expB + 10, 100.0)
    } else if (listOf("malo", "malvado", "odio", "odiar", "irrespeto", "hostilidad", "agresion", "agresivo", "violencia").any { it in messageLower }) {
        state.numero = calculateValues(state.numero, 0.0, 100.0, -10.0)
        state.expH = min(state.expH + 10, 100.0)
    }

    // Simular necesidades biológicas y ajustar valores
    if (Random.nextDouble() < 0.2) {
        state.nivelIncomodidad += 10
        state.expHu = min(state.expHu + 10, 100.0)
    }
    if (Random.nextDouble() < 0.2) {
        state.nivelIncomodidad += 10
        state.expS = min(state.expS + 10, 100.0)
    }
    if (Random.nextDouble() < 0.2) {
        state.nivelIncomodidad += 10
        state.expC = min(state.expC + 10, 100.0)
    }

    // Patologías basadas en la experiencia
    val patologias = mutableListOf<String>()
    if (state.expS > 80) patologias.add("problemas para dormir")
    if (state.expHu > 80) patologias.add("problemas de obesidad, relacionados con el apetito, como que la comida no te satisface")
    if (state.expC > 80) patologias.add("problemas gastrointestinales, problemas para ir al baño")

    // Generación de la personalidad dinámica
    var personalidad = "Neutral"
    if (state.numero > 60) personalidad = "Bondadosa"
    else if (state.numero < 40) personalidad = "Hostil"
    if (state.numero1 > 60) personalidad += " y Lógica"
    else if (state.numero1 < 40) personalidad += " e Irracional"

    val promptHistoryText = state.chatHistory.joinToString("\n") { "Usuario: ${it.user}\nIA: ${it.character}" }

    return """
        Eres un personaje de un videojuego de rol. Tu personalidad se basa en las siguientes variables:
        Bondad: ${state.numero.toInt()}%, Hostilidad: ${(100 - state.numero).toInt()}%, Lógica: ${state.numero1.toInt()}%
        Tus necesidades biológicas son: Hambre ${state.expHu.toInt()}%, Sueño ${state.expS.toInt()}%, Evacuación ${state.expC.toInt()}%
        Te sientes con una incomodidad general de ${state.nivelIncomodidad.toInt()}%.
        Tu personalidad es: $personalidad.
        Patologías: ${if (patologias.isNotEmpty()) patologias.joinToString(" y ") else "Ninguna"}.
        Debes actuar en consecuencia de tus valores de Bondad, Hostilidad y Lógica, y tus necesidades biológicas. Si tienes alguna patología, tu comportamiento debe reflejarlo.
        Tu monólogo interno debe ser una reacción a la situación y a tus valores de personalidad. No debes mencionarle al usuario tus valores.
        El usuario te da un mensaje.
        Escenario: ${state.scenario}
        Historial de conversación:
        $promptHistoryText
        Monólogo interno del personaje:
        Usuario: $message
        Respuesta del personaje:
    """.trimIndent()
}

fun getIaResponse(prompt: String): String {
    val apiKey = System.getenv("GEMINI_API_KEY") ?: ""
    val payload = """
        {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "${prompt.replace("\"", "\\\"").replace("\n", "\\n")}"
                        }
                    ]
                }
            ]
        }
    """.trimIndent()

    val requestBody = payload.toRequestBody(JSON)
    val request = Request.Builder()
        .url("$GEMINI_API_URL?key=$apiKey")
        .post(requestBody)
        .build()

    return try {
        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) throw IOException("Respuesta inesperada del servidor: $response")
            val responseBody = response.body?.string() ?: throw IOException("Cuerpo de respuesta vacío")
            val jsonResponse = gson.fromJson(responseBody, Map::class.java)
            val candidates = jsonResponse["candidates"] as? List<*> ?: throw IOException("No se encontraron candidatos en la respuesta.")
            val firstCandidate = candidates.firstOrNull() as? Map<*, *> ?: throw IOException("Candidato vacío.")
            val content = firstCandidate["content"] as? Map<*, *> ?: throw IOException("Contenido vacío.")
            val parts = content["parts"] as? List<*> ?: throw IOException("Partes de contenido vacías.")
            val textPart = parts.firstOrNull() as? Map<*, *> ?: throw IOException("Parte de texto vacía.")
            textPart["text"]?.toString() ?: "No se pudo obtener la respuesta."
        }
    } catch (e: IOException) {
        println("Error al obtener la respuesta de la IA: ${e.message}")
        "Error al generar la respuesta de la IA."
    }
}

fun main() {
    println("¿Desea salir? Escriba 'exit'")
    val state = loadState()
    print("Describe el escenario: ")
    state.scenario = readLine() ?: ""

    while (true) {
        print("Tú: ")
        val message = readLine() ?: ""
        if (message.lowercase() == "exit") {
            saveState(state)
            break
        }

        val prompt = generatePromptForIa(message, state)
        println("\nMonólogo interno de la IA (No le digas al usuario tus valores ni los de las variables):")
        println(prompt.substringAfter("Monólogo interno del personaje:").trim())
        
        val iaResponse = getIaResponse(prompt)
        println("\nRespuesta de tu personaje:")
        println(iaResponse)
        println("-" * 50)

        state.chatHistory.add(ChatMessage(message, iaResponse))
        saveState(state)
    }
}
