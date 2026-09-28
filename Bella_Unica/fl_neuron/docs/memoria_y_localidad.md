
# Memoria y localidad en NS

## Nota técnica sobre el uso de memoria del motor NS

### Contexto

NS es un intérprete de bytecode con dispatch jerárquico branchless y
dominios ortogonales. Este documento analiza el uso de memoria del
motor y lo compara con lenguajes interpretados clásicos.

---

## 1. Layout de memoria

El motor reserva los siguientes espacios en `.bss`:

| Espacio          | Offset       | Tamaño   | Propósito                     |
|------------------|--------------|----------|-------------------------------|
| `var_space`      | `0x00000000` | 16 MB    | Neuronas (8 bytes c/u)        |
| `logic_vars`     | `0x01000000` | ~16 MB   | Banderas del sistema (8 B c/u)|
| `loop_stack`     | `0x02000000` | ~2 KB    | Pila de bucles                |
| `loop_depth`     | `0x02000800` | 1 byte   | Profundidad actual            |
| `function_space` | `0x02000802` | ~16 MB   | Direcciones de funciones      |
| `function_args`  | `0x03000802` | ~16 MB   | Argumentos de funciones       |
| `function_stack` | `0x03001002` | ~16 MB   | Pila de llamadas              |
| `pointer_space`  | `0x03001804` | ~16 MB   | Punteros (8 bytes c/u)        |
| `string_space`   | `0x04001804` | ~16 MB   | Strings (32 bytes c/u)        |
| **Total**        |              | **~128 MB** | Memoria virtual reservada  |

---

## 2. Memoria virtual vs memoria física

### `.bss` no ocupa disco ni RAM física

`.bss` es la sección de **memoria no inicializada**. El sistema
operativo:

1. Reserva el **address space** del proceso (128 MB de direcciones
   virtuales).
2. **No asigna páginas físicas** hasta que se tocan.
3. Solo las páginas efectivamente accedidas se cargan en RAM.

Eso significa:

- **Binario en disco**: unos pocos KB (solo `.text` + `.data`).
- **Memoria virtual**: 128 MB reservados.
- **Memoria física**: solo las páginas tocadas (<1 MB típicamente).

---

## 3. Comparación con lenguajes interpretados clásicos

### Memoria por objeto

| Lenguaje | Tamaño mínimo por objeto | Header | Overhead |
|----------|--------------------------|--------|----------|
| Python   | 28-56 bytes              | Sí     | Alto     |
| Java     | 16-24 bytes              | Sí     | Medio    |
| Node.js  | 40-80 bytes              | Sí     | Alto     |
| **NS**   | **8 bytes**              | **No** | **Nulo** |

### Memoria del runtime

| Lenguaje | Runtime base | Programa simple |
|----------|--------------|-----------------|
| Python   | ~10-20 MB    | ~30-50 MB       |
| Java     | ~50-100 MB   | ~100-200 MB     |
| Node.js  | ~30-50 MB    | ~50-100 MB      |
| **NS**   | **0 MB**     | **<1 MB físico**|

### Memoria total (programa simple)

| Lenguaje | Virtual | Física | Disco  |
|----------|---------|--------|--------|
| Python   | ~50 MB  | ~30 MB | ~10 MB |
| Java     | ~200 MB | ~100 MB| ~50 MB |
| Node.js  | ~100 MB | ~50 MB | ~30 MB |
| **NS**   | ~128 MB | **<1 MB** | **<100 KB** |

---

## 4. Accesos a memoria por opcode

### Intérprete clásico

Un intérprete clásico (CPython, JVM, etc.) hace **múltiples accesos
a memoria por opcode**:

1. **Dispatch loop**: leer el opcode de la instruction stream.
2. **Flag register**: consultar el flag de la operación anterior.
3. **Branch unit**: decidir el salto.
4. **Memory access**: acceder a los datos.

Eso son **4 accesos a memoria** por opcode, cada uno con su propio
coste de cache miss, TLB miss, etc.

### NS

NS hace **1 acceso a memoria por opcode** (los datos), y **0** si
el opcode es branchless puro:

1. **Dispatch branchless**: leer el opcode Y ejecutar en la misma
   secuencia (sin separación dispatch/ejecución).
2. **Estado del sistema**: los flags se escriben en la misma
   operación.
3. **Branch**: solo si cambias de dominio.
4. **Memory access**: cada dominio tiene su propio espacio, con
   localidad.

Eso es **4× menos accesos a memoria** que un intérprete clásico.

---

## 5. Localidad de datos por dominio

Los espacios de memoria están separados por dominio:

- `var_space` → neuronas.
- `logic_vars` → banderas del sistema.
- `pointer_space` → punteros.
- `string_space` → strings.

Eso da **localidad de datos por dominio**:

- Cada dominio toca su propio espacio.
- No hay falsos compartidos entre dominios.
- La data cache tiene localidad.
- El TLB tiene entradas separadas por dominio.

Es exactamente lo que hacen los kernels y las bases de datos:
separar los espacios de memoria por subsistema para maximizar la
localidad.

---

## 6. La analogía del edificio

Un intérprete clásico es como un edificio con habitaciones separadas:

1. **Habitación 1**: dispatch loop (leer opcode).
2. **Habitación 2**: flag register (consultar flag).
3. **Habitación 3**: branch unit (decidir salto).
4. **Edificio 4**: memory access (acceder a datos).

Para una sola operación, el CPU tiene que **caminar por cuatro
habitaciones y un edificio**. Cada caminata es un acceso a memoria,
con su coste de cache miss y TLB miss.

NS es como una habitación única donde todo está a mano:

1. **Misma habitación**: dispatch branchless (leer + ejecutar).
2. **Misma habitación**: estado del sistema (escribir flag).
3. **Branch**: solo si cambias de dominio.
4. **Memory access**: localidad por dominio.

Una habitación para la mayoría de operaciones. Solo cambias de
habitación cuando cambias de dominio.

---

## 7. Conclusión

NS usa:

- **Más memoria virtual** (128 MB reservados), pero es gratis.
- **Menos memoria física** (<1 MB por programa).
- **Menos accesos a memoria por opcode** (1 vs 4).
- **Mejor localidad de datos** (espacios separados por dominio).

Y todo eso sin runtime, sin GC, sin VM, sin headers por objeto. El
coste es 8 bytes por neurona, 8 bytes por flag, 8 bytes por puntero.
Nada más.

La razón por la que NS es rápido no es solo el dispatch branchless
O(2K), sino que **accede a memoria 4× menos** que un intérprete
clásico. Y eso es lo que importa en hardware moderno, donde el cuello
de botella no es la CPU, sino la memoria.

---

## Referencias

- Drepper, U. (2007). *What every programmer should know about memory*.
- Gregg, B. (2013). *Systems Performance: Enterprise and the Cloud*.
- Documentación interna: `docs/dispatch_jerarquico_branchless.md`.

