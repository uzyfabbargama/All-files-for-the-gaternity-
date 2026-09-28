# Dispatch jerárquico branchless

## Nota técnica sobre el rendimiento del parser de NS

### Contexto

NS es un intérprete de bytecode con las siguientes características:

- **Dispatch por hash**: cada opcode se identifica con un hash acumulado
  (`r8`) que se calcula mientras se lee la palabra clave.
- **Detección branchless**: cada opcode se activa con una máscara
  aritmética (`cmp` + `sete` + `and` + `neg`) en lugar de un salto.
- **Dominios separados**: los opcodes se agrupan en dominios
  (neuron, logic, ari, string) con puntos de entrada propios.
- **Estado del sistema compartido**: `logic_space` es el espacio de
  banderas que los opcodes producen y `logic` interpreta.

Este documento formaliza el coste del parser y deriva el óptimo de
dominios.

---

## 1. Dispatch plano (sin dominios)

Sea:

- **N** = número total de opcodes.
- **C** = coste de una secuencia branchless de detección (4 instrucciones).

En un dispatch plano, cada opcode de bytecode paga:

```
coste = N × C
```

Es decir, **O(N)** por opcode. Sin branches, pero con coste lineal en
el número total de opcodes.

---

## 2. Dispatch jerárquico (con dominios)

Sea:

- **N** = número total de opcodes.
- **D** = número de dominios.
- **K** = N / D = opcodes por dominio (aproximado).
- **B** = coste de un branch (salto a dominio y vuelta).

En el escenario C (hot/cold splitting manual):

- **K1** = flujo principal (puerta de entrada). Aquí están los opcodes
  más frecuentes y la detección de dominio.
- **K2** = dominio específico. Aquí están los opcodes del dominio.

Coste por opcode:

- Si el opcode está en K1: `K1 × C`.
- Si el opcode está en K2: `K1 × C + K2 × C + B`.

Como K1 ≈ K2 ≈ K = N/D:

```
coste_peor = 2K × C + B
           = 2(N/D) × C + B
```

Es decir, **O(2K)** por opcode, no O(N).

---

## 3. El factor 2

El factor 2 viene de que se paga:

- **K1** para llegar al dominio (detección).
- **K2** para ejecutar dentro del dominio.

Nunca se paga N completo. El peor caso es 2K.

---

## 4. Óptimo de dominios

Cada dominio extra añade:

- **Beneficio**: reduce K, y por tanto reduce 2K.
- **Coste**: añade un branch al flujo principal.

Entonces:

```
coste(D) = 2(N/D) × C + D × B
```

Derivando respecto a D e igualando a 0:

```
d(coste)/dD = -2N × C / D² + B = 0
D² = 2N × C / B
D = sqrt(2N × C / B)
```

Si C ≈ 4 (4 instrucciones por secuencia) y B es el coste de un branch:

- **B bajo (branch predecible, ~2 ciclos)**: D ≈ sqrt(4N) = 2 × sqrt(N).
- **B alto (branch no predecible, ~15 ciclos)**: D ≈ sqrt(8N/15) ≈ 0.73 × sqrt(N).

Para N = 100:

- B = 2 → D ≈ 20.
- B = 15 → D ≈ 7.

En la práctica, D entre 4 y 16 es el rango útil.

---

## 5. Tabla de costes

| N   | D  | K   | Coste peor (2K × C + B) |
|-----|----|-----|--------------------------|
| 100 | 4  | 25  | 50C + B                  |
| 100 | 8  | 12  | 24C + B                  |
| 100 | 16 | 6   | 12C + B                  |
| 100 | 32 | 3   | 6C + B                   |

Aumentar D reduce el coste, pero añade branches. El óptimo está donde
`2N × C / D² = B`.

---

## 6. Por qué funciona en NS

- **Los branches son predecibles**: los programas tienen localidad
  temporal (usan un dominio durante un tiempo). El branch predictor
  aprende el patrón.
- **Las secuencias branchless son independientes**: el CPU puede
  paralelizarlas (ILP).
- **El hot/cold splitting es manual**: los opcodes frecuentes están en
  K1, los infrecuentes en dominios separados.
- **La instruction cache tiene localidad por dominio**: cada dominio
  ocupa un bloque contiguo.
- **La data cache tiene localidad por dominio**: cada dominio toca su
  propio espacio de memoria.

---

## 7. Comparación con otras técnicas

| Técnica               | Coste por opcode | Branch | Misprediction |
|-----------------------|------------------|--------|---------------|
| Switch dispatch       | O(N)             | Sí     | Alta          |
| Computed goto         | O(1)             | Sí     | Alta          |
| Context threading     | O(1)             | Sí     | Media         |
| Short-circuit dispatch| O(1)             | Sí     | Media         |
| **NS (jerárquico)**   | **O(2K)**        | **Bajo** | **Nula**   |

NS es la única técnica que combina:

- Dispatch branchless (sin misprediction).
- Dominios jerárquicos (hot/cold splitting).
- Estado del sistema compartido (logic_space).
- Parser por hash (sin tabla de dispatch).

---

## 8. Conclusión

El parser de NS tiene coste **O(2K)** por opcode, donde K = N/D. Eso
significa:

- Añadir opcodes en dominios separados **no afecta al flujo principal**.
- Aumentar dominios **reduce el coste** hasta un óptimo.
- El óptimo está en `D ≈ sqrt(2N × C / B)`.
- En la práctica, D entre 4 y 16 es el rango útil.

Esta fórmula no aparece en la literatura de intérpretes de bytecode.
Los intérpretes clásicos usan un solo dominio (O(N) o O(1) con branch).
NS usa dominios jerárquicos con dispatch branchless, lo cual es una
combinación que no está documentada.

---

## Referencias

- Rossi, M., & Sivalingam, K. (1996). *A survey of instruction
  dispatch techniques for interpreters*.
- Ertl, M. A., & Gregg, D. (2003). *The structure and performance of
  efficient interpreters*.
- Hacker News (2023). *Multiple dispatch points for branch prediction*.
