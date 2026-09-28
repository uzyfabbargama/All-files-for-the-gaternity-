# NeuralScript (fl_neuron) - Programming Language

**Un lenguaje de programación para redes neuronales de 56 bits con un arquitectura modular y extreme programming**

---

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Arquitectura de Cuatro Pilares](#arquitectura-de-cuatro-pilares)
- [Instalación y Compilación](#instalación-y-compilación)
- [Conceptos Fundamentales](#conceptos-fundamentales)
- [Instrucciones Disponibles](#instrucciones-disponibles)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Filosofía de Extreme Programming](#filosofía-de-extreme-programming)
- [Evolución del Proyecto](#evolución-del-proyecto)

---

## 🧠 Descripción General

**NeuralScript (fl_neuron)** es un lenguaje de programación de **bajo nivel** diseñado específicamente para:

- **Operaciones neuronales** en precisión de **56 bits**
- **Gestión de memoria extrema** con espacios confinados y punteros directos
- **Lógica condicional branchless** para máximo rendimiento
- **Procesamiento paralelizable** de redes neuronales

El lenguaje funciona como un **motor bytecode** que se compila a **x86-64 Assembly** y se ejecuta directamente en el procesador. El pipeline es:

```
Código NeuralScript (.ns) 
    ↓
Preprocesador (tokenización + macros)
    ↓
Motor XORID (lexing + tokenizing simultáneo)
    ↓
Parser x86-64
    ↓
Bytecode Binario
    ↓
Ejecución Nativa
```

---

## 🏗️ Arquitectura de Cuatro Pilares

### 1. **Motor XORID (Lexer + Tokenizer Unificado)**

El corazón del lenguaje. Combina análisis léxico y tokenización en **una sola pasada**.

**Características:**
- **XOR Hashing**: Cada palabra clave tiene un hash único calculado con XOR
- **Lectura de 8 bytes**: Procesa tokens de hasta 8 caracteres simultáneamente
- **Branchless**: Sin saltos condicionales en el loop principal

**Hashes de Palabras Clave:**
```
var     = 720      # Declaración de neurona
proc    = 1514     # Procesamiento neuronal
decay   = 2238     # Reducción de valor
growth  = 5064     # Aumento de valor
logic   = 2346     # Bloque lógico/condicional
conv    = 1052     # Convolución
norm    = 1162     # Normalización
drop    = 1164     # Dropout determinista
cmp     = 588      # Comparación
loop    = 1252     # Bucle condicional
endloop = 9592     # Fin de bucle
```

---

### 2. **Motor de Redes Neuronales (56 bits)**

Memoria especializada para neuronas con precisión fraccionaria en 56 bits.

**Estructura de una Neurona:**
```
┌─────────────────────────────────────┐
│        56 BITS DE VALOR             │
├─────────────────────────────────────┤
│ Bit 55-8: Mantisa (valores)        │
│ Bit 7-0:  Flag de Disparo (0/1)    │
└─────────────────────────────────────┘
```

**Operaciones Principales:**
- **PROC**: Multiplica dos neuronas, aplica AND bitwise y suma acumulada. Dispara si resultado > threshold
- **DECAY/GROWTH**: Ajusta la mantisa sin afectar el flag de disparo
- **CONV**: Convolución: `resultado = (n1 * n2) + bias`
- **NORM**: Normalización branchless usando resta recursiva

**Espacios de Memoria:**
```
var_space (16 MB)      → Almacena valores de neuronas
logic_vars (16 MB)     → Variables condicionales (booleanas)
```

---

### 3. **Motor Lógico (Logic Space)**

Sistema de control basado en **lógica branchless** para máximo rendimiento.

**Características:**
- **Condicionales sin branching**: Usa operaciones bitwise para evitar saltos
- **Bucles anidados**: Stack de punteros para hasta 256 niveles de anidación
- **Funciones locales**: `logic def` permite definir funciones con scope local
- **Predicados**: `logic yes` / `logic no` para ejecución condicional

**Instrucciones Lógicas:**
```
logic cmp var_cond, n1, n2     # Compara n1 == n2, guarda en var_cond
logic cmpv var_cond, n1, valor # Compara n1 == valor_constante
logic cmpn var_cond, neurona   # Verifica si flag de disparo está activo
logic loop var_cond            # Bucle mientras var_cond sea verdadera
logic endloop                  # Cierra bucle
logic prom dest, n1, n2        # Promedio: (n1 + n2) >> 1
logic def func_id              # Define función
logic use func_id              # Llama función
logic yes/no var_cond          # Ejecuta condicionalmente
logic endcond                  # Cierra condicional
```

---

### 4. **Aritmética (Arithmetic Mode)**

Gestión directa de punteros para acceso confinado a variables.

**Característica Innovadora: Punteros Relativos**

```
ari var p, 1              # Crea puntero en posición 1
var n[p], 0.34            # Variable relativa al puntero
var n2, 0.33              # En posición p + 1
ari add p, 5              # Avanza puntero
ari sub p, 2              # Retrocede puntero
ari lim cond, p, 100      # Verifica si p < 100
```

El preprocesador **convierte automáticamente** referencias con punteros:
```
var n[p], val  →  var n[ID + p], val
```

**Utilidad:** Permite iteración segura sobre arrays sin usar bucles explícitos.

---

## 🚀 Instalación y Compilación

### Requisitos
- `nasm` (Netwide Assembler)
- `gcc` o `ld` (Linker)
- Python 3.6+
- Linux x86-64

### Compilar el Motor

```bash
cd Bella_Unica/fl_neuron
bash compilar
```

**compilar** (script):
```bash
#!/bin/bash
nasm -f elf64 NeuralScriptv6.asm -o NSMotor.o
ld -shared NSMotor.o -o libNSMotor.so
gcc -c NSMotor.py -o NSMotor.o
```

### Usar el Lenguaje

```bash
python3 preprocesador_v8.py mi_programa.ns
python3 motor_neuralscript.py bytecode.bin
```

---

## 💡 Conceptos Fundamentales

### Variables Neuronales (var)

```
var neurona, 0.5      # Crea neurona con valor 0.5
var n1, 1.34
var n2, 0.783
```

Internamente: Almacenado en `var_space` con indexación directa.

### Procesamiento (proc)

```
proc destino, fuente1, fuente2
```

**Fórmula:**
```
r15 = (fuente1 AND fuente2)
r15 = fuente1 + r15 + fuente2 + r15 + fuente2 + r15 + ...
disparar = (r15 << 1) >> 55 & 1
destino[bit7] = disparar
```

Resultado: "Dispara" si el procesamiento cruza el threshold.

### Convolución (conv)

```
conv neurona1, neurona2, bias
```

**Operación:** `neurona1 = (neurona1 * neurona2) + bias`

Equivalente a capas convolucionales en redes neuronales tradicionales.

### Normalización (norm)

```
norm n1, n2
```

**Algoritmo Branchless:**
```
diferencia = n1 XOR n2
n1 = n1 - diferencia
n2 = n2 - diferencia
n2 = n2 - n1
diferencia = diferencia - n2
resultado = diferencia + EPSILON  # Epsilon = 1 para evitar división por cero
```

---

## 📚 Instrucciones Disponibles

### Instrucciones de Variables

| Instrucción | Sintaxis | Descripción |
|-----------|---------|-------------|
| `var` | `var nombre, valor` | Declara neurona con valor inicial |
| `proc` | `proc dest, n1, n2` | Procesa dos neuronas |
| `decay` | `decay neurona, valor` | Reduce el valor de una neurona |
| `growth` | `growth neurona, valor` | Aumenta el valor de una neurona |
| `conv` | `conv n1, n2, bias` | Convolución |
| `norm` | `norm n1, n2` | Normalización |
| `drop` | `drop n1, n2` | Dropout determinista |

### Instrucciones Lógicas

| Instrucción | Sintaxis | Descripción |
|-----------|---------|-------------|
| `logic cmp` | `logic cmp cond, n1, n2` | Compara n1 == n2 |
| `logic cmpv` | `logic cmpv cond, n1, val` | Compara n1 == valor |
| `logic cmpn` | `logic cmpn cond, neurona` | Verifica flag de disparo |
| `logic loop` | `logic loop cond` | Bucle condicional |
| `logic endloop` | - | Cierra bucle |
| `logic prom` | `logic prom dest, n1, n2` | Promedio entero |
| `logic def` | `logic def func_id (arg=val)` | Define función |
| `logic use` | `logic use func_id` | Llama función |
| `logic yes/no` | `logic yes/no cond` | Ejecuta si verdadero/falso |
| `logic endcond` | - | Cierra condicional |

### Instrucciones de Aritmética

| Instrucción | Sintaxis | Descripción |
|-----------|---------|-------------|
| `ari var` | `ari var ptr, valor` | Declara puntero |
| `ari add` | `ari add ptr, valor` | Avanza puntero |
| `ari sub` | `ari sub ptr, valor` | Retrocede puntero |
| `ari lim` | `ari lim cond, ptr, limite` | Verifica límite |

---

## 📖 Ejemplos de Uso

### Ejemplo 1: Red Neuronal Simple

```
var n1, 0.5
var n2, 0.7
var resultado, 0.0

proc resultado, n1, n2

logic cmp condicion, n1, n2
logic yes condicion
    growth resultado, 0.2
logic endcond
```

### Ejemplo 2: Bucle Condicional

```
var i, 0.0
var limite, 10.0
var suma, 0.0

logic loop ciclo
    growth suma, 0.1
    decay i, -1.0
    logic cmpv condicion, i, 10.0
    logic yes condicion
        logic endloop
    logic endcond
logic endloop
```

### Ejemplo 3: Convolución

```
var kernel, 0.3
var input, 0.5
var bias, 0.1
var output, 0.0

conv output, input, bias
conv output, kernel, 0.0
```

### Ejemplo 4: Normalización

```
var a, 0.8
var b, 0.6

norm a, b
# a y b ahora están normalizados (diferencia minimizada)
```

### Ejemplo 5: Función Personalizada

```
logic def suma_neuronas (tmp = local_var)
    proc tmp, n1, n2
    growth tmp, 0.05
logic endef

var n1, 0.3
var n2, 0.7

logic use suma_neuronas
```

---

## ⚡ Filosofía de Extreme Programming

NeuralScript implementa principios de **Extreme Programming (XP)** desde el hardware:

### 1. **Simplicidad Radical**
- Solo 4 módulos claramente separados
- Cada instrucción hace exactamente una cosa
- Sin abstracciones innecesarias

### 2. **Branchless Programming**
- Cero saltos condicionales en loops críticos
- Operaciones XOR/AND en lugar de `if/else`
- Máximo paralelismo de instrucciones

### 3. **Testing Continuo**
- Carpeta `test_*.py` con validaciones de cada operación
- `test_conv.py`, `test_proc.py` verifican correctitud
- Output de precisión 56-bit verificable

### 4. **Refactoring Agresivo**
- Evolución clara: v1 → v2 → v3 → v4 → v5 → v6
- Cada versión añade funcionalidad incrementalmente
- `preprocesador_v1` → `preprocesador_v8` muestran mejoras

### 5. **Pair Programming a Nivel de Hardware**
- Motor XORID + Logic Space trabajan en sincronía
- Memoria compartida (`var_space` ↔ `logic_vars`)
- Pasos definidos y predecibles

---

## 🔄 Evolución del Proyecto

### v1: MVP - Motor Básico
- Instrucciones fundamentales: `var`, `proc`, `decay`, `growth`, `logic cmp`
- Parser básico con hashing XOR
- Soporte para comparaciones simples

**Archivo:** `NeuralScriptv1.asm` (3.4 KB)

### v2: Lógica Avanzada
- Loops anidados branchless
- Stack para profundidad de bucles
- Predicados `logic yes/no`
- Arquitectura de función separada para `logic_mode`

**Archivo:** `NeuralScriptv2.asm` (7.8 KB)

### v3: Operaciones Neuronales Extendidas
- `conv`: Convolución
- `norm`: Normalización branchless
- `drop`: Dropout determinista
- Mejor manejo de memoria

**Archivo:** `NeuralScriptv3.asm` (8.7 KB)

### v4: Motor Relocatable
- Función llamable `NSMotor(rdi=bytecode)`
- Soporte para librería compartida `.so`
- Acceso dinámico a memoria base
- Preprocesador mejorado

**Archivo:** `NeuralScriptv4.asm` (23.6 KB)

### v5: Funciones Locales
- `logic def`: Definición de funciones con scope local
- `logic use`: Invocación de funciones
- Variables de argumento locales
- Stack de recursión para hasta 256 niveles

**Archivo:** `NeuralScriptv5.asm` (30.2 KB)

### v6: Optimización Final
- Inline de predicados frecuentes
- Caché de punteros de función
- Mejor balanceo de registros
- Preprocesador v8 con macros full-featured

**Archivo:** `NeuralScriptv6.asm` (34.6 KB)

---

## 📁 Estructura del Proyecto

```
fl_neuron/
├── NeuralScriptv1.asm         # v1: MVP
├── NeuralScriptv2.asm         # v2: Lógica
├── NeuralScriptv3.asm         # v3: Operaciones
├── NeuralScriptv4.asm         # v4: Motor relocatable
├── NeuralScriptv5.asm         # v5: Funciones
├── NeuralScriptv6.asm         # v6: Optimizado
├── preprocesador_v1.py        # v1: Basic
├── preprocesador_v2.py        # v2: Tokens
├── preprocesador_v3.py        # v3: Macros
├── preprocesador_v4.py        # v4: Simplify
├── preprocesador_v5.py        # v5: Expand
├── preprocesador_v6.py        # v6: Optimized
├── preprocesador_v7.py        # v7: Cleaner
├── preprocesador_v8.py        # v8: Full Featured
├── motor_neuralscript.py      # Ejecutor
├── test_conv.py               # Prueba convolución
├── test_proc.py               # Prueba procesamiento
├── test_NS.py                 # Prueba integración
├── bella_neuronal.py          # Utilidades
├── macrosy12.py               # Macro processor
├── tokenizador.py             # Tokenizer test
├── compilar                   # Build script
├── doc_tests.txt              # Salidas de pruebas
├── docbytecode.md             # Referencia bytecode
├── tutorial.txt               # Tutorial básico
├── README.md                  # Este archivo
└── docs/                      # Documentación
```

---

## 🧪 Pruebas

### Ejecutar Pruebas

```bash
# Convolución
python3 test_conv.py

# Procesamiento
python3 test_proc.py

# Integración
python3 test_NS.py
```

### Salida Esperada

```
Convolución:
Primer valor: 3.4
Segundo valor: 6.7
Bias: 3.4
→ 1.9000000000000012

Procesamiento:
Neurona A: 0.5 | Neurona B: 0.5
Bit de Disparo (r9): 1
Acumulado resultante en R13: 0.0000000000
```

---

## 🎯 Casos de Uso

### 1. **Procesamiento de Redes Neuronales Profundas**
Ejecutar modelos entrenados con precisión de 56 bits en tiempo real

### 2. **Análisis de Series Temporales**
Procesar streams continuos de datos con bucles anidados eficientes

### 3. **Sistemas Embebidos**
Bajo nivel de memoria, ejecución nativa sin intérprete

### 4. **Modelado de Comportamiento**
Simulación de sistemas dinámicos con convoluciones

### 5. **Prototipado Rápido**
Macro system permite iteración rápida sin recompilación

---

## 🔧 Desarrollo

### Agregar Nueva Instrucción

1. **Elegir nuevo hash**: Calcular `XOR(palabra)` de la instrucción
2. **Implementar en ASM**: Añadir comparación en `manager_state` o `logic_mode`
3. **Actualizar preprocesador**: Agregar en `preprocesador_v8.py`
4. **Testear**: Crear `test_nueva.py`
5. **Documentar**: Actualizar este README

### Ejemplo: Instrucción `add` (suma simple)

```asm
; add n1, n2, resultado
; Hash: 611 (ejemplo)
mov rax, r8
cmp rax, 611
sete al
and rax, 1
neg rax

mov r14d, [rdi+rsi]
shr r14d, 11
and r14d, eax
mov rcx, 3
and rcx, rax
add rsi, rcx

mov r13d, [rdi+rsi]
shr r13d, 11
and r13d, eax
mov rcx, 3
and rcx, rax
add rsi, rcx

mov r12, [rbx+r14*8]
add r12, [rbx+r13*8]
mov [rbx+r14*8], r12
```

---

## 📝 Licencia

Este proyecto es parte de **"Gaternity"** archive. Usos educativos y de investigación permitidos.

---

## 👨‍💻 Autor

**Uziel Gamma (uzyfabbargama)**

Proyecto: Bella_Unica - Extreme Programming en Neuron-Level

---

## 🤝 Contribuciones

Para contribuir:

1. Entender la arquitectura de 4 pilares
2. Mantener principios de XP
3. Agregar tests para cada cambio
4. Documentar en README
5. Versionar como `NeuralScriptv7.asm`, etc.

---

## 📚 Referencias

- **Bytecode Reference**: `docbytecode.md`
- **Tutorial**: `tutorial.txt`
- **Test Outputs**: `doc_tests.txt`
- **Hash IDs**: `hash_id_kw.txt`
- **Example Programs**: `coordinador.ns.txt`, `red_atencion.ns`

---

**🚀 ¡Bienvenido al futuro del extreme programming a nivel de hardware! 🚀**
